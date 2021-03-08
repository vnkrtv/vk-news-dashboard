import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output


class Layout:
    Navbar: html.Div = html.Div([
        html.A(className="navbar-brand", children=[
            html.Strong('VK News Dashboard')
        ],
               style={'position': 'absolute', 'margin-top': '0.5vh'})
    ],
        className='navbar navbar-dark bg-dark shadow-sm', style={'height': '5vh'})

    WordCloudPlots: html.Div = [
        dbc.CardHeader(html.H5("Most frequently used words in complaints")),
        dbc.Alert(
            "Not enough data to render these plots, please adjust the filters",
            id="no-data-alert",
            color="warning",
            style={"display": "none"},
        ),
        dbc.CardBody(
            [
                dbc.Row(
                    [
                        dbc.Col(
                            dcc.Loading(
                                id="loading-frequencies",
                                children=[dcc.Graph(id="frequency_figure")],
                                type="default",
                            )
                        ),
                        dbc.Col(
                            [
                                dcc.Tabs(
                                    id="tabs",
                                    children=[
                                        dcc.Tab(
                                            label="Treemap",
                                            children=[
                                                dcc.Loading(
                                                    id="loading-treemap",
                                                    children=[dcc.Graph(id="bank-treemap")],
                                                    type="default",
                                                )
                                            ],
                                        ),
                                        dcc.Tab(
                                            label="Wordcloud",
                                            children=[
                                                dcc.Loading(
                                                    id="loading-wordcloud",
                                                    children=[
                                                        dcc.Graph(id="bank-wordcloud")
                                                    ],
                                                    type="default",
                                                )
                                            ],
                                        ),
                                    ],
                                )
                            ],
                            md=8,
                        ),
                    ]
                )
            ]
        ),
    ]
