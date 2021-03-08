import asyncio
import threading
from typing import List, Any

import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

from . import config as cfg
from . import graphs
from .preprocessing import TextProcessor
from .entities_extractor import EntitiesExtractor
from .postgres import Storage
from .layout import Layout

app = dash.Dash(
    'VK News',
    meta_tags=[{"name": "viewport", "content": "width=device-width"}],
    external_stylesheets=[dbc.themes.DARKLY],
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

app.layout = html.Div([
    Layout.Navbar,
    html.Div([
        html.Div([
            html.Div([
                dbc.Card([
                    html.Div([
                        html.H4('Группа'),
                        dcc.Dropdown(
                            options=[
                                {'label': groups_df.iloc[i]['name'], 'value': groups_df.iloc[i]['name']}
                                for i in range(len(groups_df))
                            ],
                            value=groups_df.iloc[0]['name'],
                            id='group-select',
                            style={'color': 'black'})
                    ],
                        style={'margin': '1vh'}),
                    html.Div([],
                             id='group-info',
                             style={'margin': '1vh'}),
                    dcc.Interval(
                                id='data-update-interval',
                                interval=1000 * cfg.DATA_UPDATING_INTERVAL,  # in milliseconds
                                n_intervals=0
                            ),
                    html.Div([],
                             style={'margin': '1vh'},
                             id='news-container')
                ], id='left-card')

            ],
                className='col-2'),
            html.Div([],
                     className='col-5',
                     id='left-plots'),
            html.Div([],
                     className='col-5',
                     id='right-plots')
        ],
            className='row')
    ],
        className='', style={'width': '97%', 'margin': '3vh'}),
    dbc.Card(Layout.WordCloudPlots)
])


@app.callback(
    Output("left-plots", "children"),
    [Input("group-select", "value")])
def left_plots_update(value) -> List[html.Div]:
    if value is None:
        return []
    group = groups_df[groups_df['name'] == value].iloc[0]
    return [
        graphs.LineCharts.views(posts_df, group),
        graphs.LineCharts.comments(posts_df, group)]


@app.callback(
    [
        Output("bank-wordcloud", "figure"),
        Output("frequency_figure", "figure"),
        Output("bank-treemap", "figure"),
        Output("no-data-alert", "style"),
    ],
    [
        Input("group-select", "value")
    ],
)
def update_wordcloud_plot(value):
    """ Callback to rerender wordcloud plot """
    wordcloud, frequency_figure, treemap = graphs.WordCloudPlot.make_wordcload(entities_df)
    alert_style = {"display": "none"}
    if (wordcloud == {}) or (frequency_figure == {}) or (treemap == {}):
        alert_style = {"display": "block"}
    print("redrawing bank-wordcloud...done")
    return (wordcloud, frequency_figure, treemap, alert_style)


@app.callback(
    Output("right-plots", "children"),
    [Input("group-select", "value")])
def right_plots_update(value) -> List[html.Div]:
    if value is None:
        return []
    group = groups_df[groups_df['name'] == value].iloc[0]
    return [
        graphs.LineCharts.likes(posts_df, group),
        graphs.LineCharts.reposts(posts_df, group)]


@app.callback(
    Output("group-info", "children"),
    [Input("group-select", "value")])
def groups_info_update(value) -> List[Any]:
    if value is None:
        return []
    group = groups_df[groups_df['name'] == value].iloc[0]
    group_posts = posts_df[posts_df['group'] == group['screen_name']]
    children = [
        html.A(f'Число подписчиков: {group["members_count"]}'),
        html.Br(),
        html.A(f'Среднее число просмотров: {int(group_posts["views_count"].mean())}'),
        html.Br(),
        html.A(f'Среднее число лайков: {int(group_posts["likes_count"].mean())}'),
        html.Br(),
        html.A(f'Среднее число комментариев: {int(group_posts["comments_count"].mean())}'),
        html.Br(),
        html.A(f'Среднее число репостов: {int(group_posts["reposts_count"].mean())}')
    ]
    return children


@app.callback(Output('news-container', 'children'),
              [Input('data-update-interval', 'n_intervals')])
def update_news(_) -> List[Any]:
    return graphs.NewsTable.update_news(posts_df, groups_df)


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
