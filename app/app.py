import dash
import dash_html_components as html
import dash_bootstrap_components as dbc
from app import config as cfg
import pandas as pd
from .graphs import groups_pie_chart
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

data = pd.DataFrame()
for group in groups_df.iterrows():
    row = {
        'groups': group[1][0],
        'posts_count': len(posts_df[posts_df['group'] == group[1][1]])
    }
    data = data.append(row, ignore_index=True)


app.layout = html.Div([
    html.Div([
        html.A(className="navbar-brand d-flex align-items-center", children=[
            html.Strong('VK News Analyzer')
        ]),
        html.Div([
            dbc.DropdownMenu([
                dbc.DropdownMenuItem('Ru'),
                dbc.DropdownMenuItem('En')
            ], label='Lang')
        ],
            className='d-flex justify-content-between')
    ],
        className='navbar'),
    html.Div([
        groups_pie_chart(data=data)
    ],
        className='container')

])
