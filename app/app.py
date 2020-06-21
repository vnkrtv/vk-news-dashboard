import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output
from . import config as cfg
from . import graphs
from .preprocessing import TextProcessor
from .postgres import (
    PostgresStorage, PostsStorage, GroupsStorage)

app = dash.Dash(
    'VK News',
    meta_tags=[{"name": "viewport", "content": "width=device-width"}],
    external_stylesheets=[dbc.themes.DARKLY],
    serve_locally=True
)

server = app.server

storage = PostgresStorage.connect(
    dbname=cfg.PG_NAME,
    user=cfg.PG_USER,
    password=cfg.PG_PASSWORD,
    host=cfg.PG_HOST,
    port=cfg.PG_PORT)
groups_storage = GroupsStorage(storage)
posts_storage = PostsStorage(storage)

posts_list = posts_storage.get_posts()
groups_list = groups_storage.get_groups()

posts_df = TextProcessor.parse_posts(posts_list)
groups_df = TextProcessor.parse_groups(groups_list)

app.layout = html.Div([
    html.Div([
        html.A(className="navbar-brand", children=[
            html.Strong('VK News Dashboard')
        ],
               style={'position': 'absolute', 'margin-top': '0.5vh'})
    ],
        className='navbar navbar-dark bg-dark shadow-sm', style={'height': '5vh'}),
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
                    graphs.NewsTable.get_news(posts_df, groups_df)
                ])

            ],
                className='col-2'),
            html.Div([
                dbc.Card([

                ], id='likes-plot')
            ],
                className='col-10')
        ],
            className='row')
    ],
        className='', style={'width': '97%', 'margin': '3vh'})

])


@app.callback(
    Output("likes-plot", "children"),
    [Input("group-select", "value")])
def plots_update(value):
    group = groups_df[groups_df['name'] == value].iloc[0]
    return graphs.LineCharts.likes(posts_df, group)


@app.callback(
    Output("group-info", "children"),
    [Input("group-select", "value")])
def groups_info_update(value):
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

