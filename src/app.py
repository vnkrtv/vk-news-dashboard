import asyncio
import threading
import logging
from datetime import datetime
from typing import List, Tuple, Any

import pandas as pd
import dash
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

from src import config as cfg
from src import plots
from src.preprocessing import TextProcessor
from src.entities_extractor import EntitiesExtractor
from src.postgres import Storage
from src.layout import Layout

logging.basicConfig(level=logging.INFO)
app = dash.Dash(
    'VK News',
    meta_tags=[{"name": "viewport", "content": "width=device-width"}],
    external_stylesheets=[dbc.themes.BOOTSTRAP],
    serve_locally=True
)

server = app.server
app.title = 'VK News Dashboard'

extractor = EntitiesExtractor()
storage = Storage.connect(
    dbname=cfg.PG_NAME,
    user=cfg.PG_USER,
    password=cfg.PG_PASS,
    host=cfg.PG_HOST,
    port=cfg.PG_PORT)

posts = storage.get_posts()
groups = storage.get_groups()
entities = storage.get_entities()

posts_df = TextProcessor.parse_posts(posts)
groups_df = TextProcessor.parse_groups(groups)
entities_df = TextProcessor.parse_entities(entities)

layout = Layout(groups=list(groups_df['name'].values), data_update_interval=cfg.DATA_UPDATING_INTERVAL)

app.layout = html.Div([
    layout.Navbar,
    dbc.Row([
        dbc.Col([
            layout.GroupCard,
            layout.NewsCard
        ],
            md=2),
        dbc.Col(layout.GroupStatPlots,
                md=5,
                style={
                    # 'margin-left': '1vh',
                    'margin-top': '1vh'
                }
                ),
        dbc.Col(layout.WordCloudCard,
                md=5,
                style={
                    # 'margin-left': '1vh',
                    'margin-top': '1vh'
                }
                )
    ],
        style={"border": "0px", "margin-right": 0, "margin-left": 0, "max-width": "100%"}
    )
])


def make_marks_time_slider(start: datetime, end: datetime):
    points_count = 6
    delta = (end - start) / points_count
    ret = {
        int((start + delta * i).timestamp()): (start + delta * i).strftime('%d-%m-%Y')
        for i in range(points_count)
    }
    return ret


def get_entities(group_name: str, entity_type: str, start_date: datetime, end_date: datetime) -> pd.DataFrame:
    group = groups_df[groups_df['name'] == group_name].iloc[0]
    group_entities = entities_df[
        entities_df['post_id'].isin(
            posts_df[posts_df['group'] == group['screen_name']]['post_id'].values
        )
        &
        (entities_df['date'] <= end_date)
        &
        (entities_df['date'] >= start_date)
    ]
    if entity_type != 'ALL':
        group_entities = group_entities[group_entities['type'] == entity_type]
    return group_entities


@app.callback(
    [
        Output("time-window-slider", "marks"),
        Output("time-window-slider", "min"),
        Output("time-window-slider", "max"),
        Output("time-window-slider", "step"),
        Output("time-window-slider", "value"),
    ],
    [Input("group-select", "value")],
)
def populate_time_slider(group_name: str):
    group = groups_df[groups_df['name'] == group_name].iloc[0]
    group_posts = posts_df[posts_df['group'] == group['screen_name']]

    min_date = group_posts["date"].min()
    max_date = group_posts["date"].max()

    marks = make_marks_time_slider(min_date, max_date)
    min_epoch = list(marks.keys())[0]
    max_epoch = list(marks.keys())[-1]

    return (
        marks,
        min_epoch,
        max_epoch,
        (max_epoch - min_epoch) / (len(list(marks.keys())) * 3),
        [min_epoch, max_epoch],
    )


@app.callback(
    [
        Output("news-wordcloud", "figure"),
        # Output("frequency_figure", "figure"),
        Output("news-treemap", "figure"),
        Output("no-data-alert", "style")
    ],
    [
        Input("group-select", "value"),
        Input("entity-type-drop", "value"),
        Input("time-window-slider", "value")
    ],
)
def update_wordcloud_plot(group_name: str, entity_type: str, timestamps: List[int]):
    group_entities = get_entities(
        group_name=group_name,
        entity_type=entity_type,
        start_date=datetime.fromtimestamp(timestamps[0]),
        end_date=datetime.fromtimestamp(timestamps[1]))
    wordcloud, frequency_figure, treemap = plots.WordCloudPlots.get_plots(group_entities)
    alert_style = {"display": "none"}
    if (wordcloud == {}) or (frequency_figure == {}) or (treemap == {}):
        alert_style = {"display": "block"}
    return wordcloud, treemap, alert_style
    # return wordcloud, frequency_figure, treemap, alert_style


@app.callback(
    [
        Output("group-views-plot", "figure"),
        Output("group-comments-plot", "figure"),
        Output("group-likes-plot", "figure"),
        Output("group-reposts-plot", "figure")
    ],
    [
        Input("group-select", "value")
    ]
)
def update_group_stat_plots(group_name: str):
    if group_name is None:
        return {}, {}, {}, {}
    group = groups_df[groups_df['name'] == group_name].iloc[0]
    group_posts = posts_df[posts_df['group'] == group['screen_name']]

    views_fig = plots.LineCharts.views(group_posts)
    comments_fig = plots.LineCharts.comments(group_posts)
    likes_fig = plots.LineCharts.likes(group_posts)
    reposts_fig = plots.LineCharts.reposts(group_posts)

    # return views_fig, comments_fig
    return views_fig, comments_fig, likes_fig, reposts_fig


@app.callback(
    Output("group-info", "children"),
    [
        Input("group-select", "value")
    ]
)
def groups_info_update(group_name: str) -> List[Any]:
    if group_name is None:
        return []
    group = groups_df[groups_df['name'] == group_name].iloc[0]
    group_posts = posts_df[posts_df['group'] == group['screen_name']]
    children = [
        html.A(f'Число подписчиков: {group["members_count"]}'),
        html.Br(),
        html.A(f'В среднем просмотров: {int(group_posts["views_count"].mean())}'),
        html.Br(),
        html.A(f'В среднем лайков: {int(group_posts["likes_count"].mean())}'),
        html.Br(),
        html.A(f'В среднем комментариев: {int(group_posts["comments_count"].mean())}'),
        html.Br(),
        html.A(f'В среднем репостов: {int(group_posts["reposts_count"].mean())}')
    ]
    return children


@app.callback(
    Output('news-container', 'children'),
    [
        Input('data-update-interval', 'n_intervals')
    ]
)
def update_news(_) -> List[Any]:
    return plots.NewsTable.update_news(posts_df, groups_df)


@asyncio.coroutine
def update_data():
    global storage, extractor, posts, groups, entities, posts_df, groups_df, entities_df
    while True:
        yield from asyncio.sleep(cfg.DATA_UPDATING_INTERVAL)

        unprocessed_posts = storage.get_unprocessed_posts()
        logging.info('Loaded %d new posts' % len(unprocessed_posts))
        new_entities = extractor.get_entities(unprocessed_posts)
        if new_entities:
            storage.add_entities(new_entities)
        logging.info('Add %d new entities' % len(new_entities))

        posts = storage.get_posts()
        groups = storage.get_groups()
        entities = storage.get_entities()

        posts_df = TextProcessor.parse_posts(posts)
        groups_df = TextProcessor.parse_groups(groups)
        entities_df = TextProcessor.parse_entities(entities)

        logging.info('Update posts and entities')


def update_data_loop(update_loop):
    asyncio.set_event_loop(update_loop)
    update_loop.run_until_complete(update_data())


loop = asyncio.get_event_loop()
t = threading.Thread(target=update_data_loop, args=(loop,))
t.start()
