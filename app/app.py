import asyncio
import threading
from typing import List, Tuple, Any

import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

from . import config as cfg
from . import plots
from .preprocessing import TextProcessor
from .entities_extractor import EntitiesExtractor
from .postgres import Storage
from .layout import Layout

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


@app.callback(
    [
        Output("news-wordcloud", "figure"),
        # Output("frequency_figure", "figure"),
        Output("news-treemap", "figure"),
        Output("no-data-alert", "style")
    ],
    [
        Input("group-select", "value")
    ],
)
def update_wordcloud_plot(group_name: str):
    if group_name is None:
        alert_style = {"display": "block"}
        return {}, {}, alert_style
    group = groups_df[groups_df['name'] == group_name].iloc[0]
    group_entities = entities_df[
        entities_df['post_id'].isin(
            posts_df[posts_df['group'] == group['screen_name']]['post_id'].values
        )
    ]
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
    data = posts_df[posts_df['group'] == group['screen_name']]

    views_fig = plots.LineCharts.views(data)
    comments_fig = plots.LineCharts.comments(data)
    likes_fig = plots.LineCharts.likes(data)
    reposts_fig = plots.LineCharts.reposts(data)

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
        new_entities = extractor.get_entities(unprocessed_posts)
        storage.add_entities(new_entities)

        posts = storage.get_posts()
        groups = storage.get_groups()
        entities = storage.get_entities()

        posts_df = TextProcessor.parse_posts(posts)
        groups_df = TextProcessor.parse_groups(groups)
        entities_df = TextProcessor.parse_entities(entities)


def update_data_loop(update_loop):
    asyncio.set_event_loop(update_loop)
    update_loop.run_until_complete(update_data())


loop = asyncio.get_event_loop()
t = threading.Thread(target=update_data_loop, args=(loop,))
t.start()
