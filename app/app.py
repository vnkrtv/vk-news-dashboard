import dash
import dash_html_components as html
import dash_bootstrap_components as dbc
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
        html.A(className="navbar-brand d-flex align-items-center", children=[
            html.Strong('VK News Analyzer')
        ]),
        html.Div([
            dbc.DropdownMenu([
                dbc.DropdownMenuItem('Ru'),
                dbc.DropdownMenuItem('En')
            ], label='Язык', className='navbar-brand nav-link', in_navbar=True)
        ],
            className='d-flex justify-content-between')
    ],
        className='navbar shadow-sm'),
    html.Div([
        html.Div([
            html.Div([
                graphs.NewsTable.get_news(posts_df, groups_df)
            ],
                className='col-2'),
            html.Div([
                graphs.LineCharts.likes(posts_df, groups_df.loc[1])
            ],
                className='col-10')
        ],
            className='row')
    ],
        className='', style={'width': '100%', 'margin': '5vh'})

])
