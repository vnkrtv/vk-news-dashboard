from typing import List

import dash_html_components as html
import dash_core_components as dcc
import dash_bootstrap_components as dbc


class Layout:
    groups: List[str]
    data_update_interval: int

    def __init__(self, groups: List[str], data_update_interval: int):
        self.groups = groups
        self.data_update_interval = data_update_interval * 1000

    @property
    def Navbar(self) -> dbc.Navbar:
        return dbc.Navbar(
            children=[
                html.A(
                    dbc.Row(
                        [
                            # dbc.Col(html.Img(src=PLOTLY_LOGO, height="30px")),
                            dbc.Col(
                                dbc.NavbarBrand("VK News Dashboard", className="ml-2")
                            ),
                        ],
                        align="center",
                        no_gutters=True,
                    ),
                    href="https://github.com/vnkrtv/vk-news-dashboard",
                )
            ],
            color="dark",
            dark=True,
            sticky="top",
        )

    @property
    def GroupCard(self) -> dbc.Card:
        return dbc.Card([
            dbc.CardHeader(html.H4('Группа')),
            dbc.CardBody([
                dcc.Dropdown(
                    options=[
                        {'label': group, 'value': group}
                        for group in self.groups
                    ],
                    value=self.groups[0],
                    id='group-select',
                    style={'color': 'black'}
                ),
                html.Div([], id='group-info'),
                dcc.Interval(
                    id='data-update-interval',
                    interval=self.data_update_interval,  # in milliseconds
                    n_intervals=0)
            ])
        ],
            style={
                'margin-left': '1vh',
                'margin-top': '1vh'
            }
        )

    @property
    def NewsCard(self) -> dbc.Card:
        return dbc.Card([],
                        style={
                            'margin-left': '1vh',
                            'margin-top': '1vh',
                            'margin-bottom': '1vh'
                        },
                        id='news-container')

    @property
    def GroupStatPlots(self) -> dbc.Card:
        return dbc.Card([
            dbc.CardHeader(html.H4("Статистика постов группы")),
            dbc.Alert(
                "Недостаточно данных для для отображения графиков",
                id="no-group-data-alert",
                color="warning",
                style={"display": "none"},
            ),
            dbc.CardBody(
                [

                    dcc.Tabs(
                        id="group-stats-plots",
                        children=[
                            dcc.Tab(
                                label="Просмотры",
                                children=[
                                    dcc.Loading(
                                        id="loading-group-views-plot",
                                        children=[dcc.Graph(id="group-views-plot")],
                                        type="default",
                                    )
                                ],
                            ),
                            dcc.Tab(
                                label="Комментарии",
                                children=[
                                    dcc.Loading(
                                        id="loading-group-comments-plot",
                                        children=[
                                            dcc.Graph(id="group-comments-plot")
                                        ],
                                        type="default",
                                    )
                                ],
                            ),
                            dcc.Tab(
                                label="Лайки",
                                children=[
                                    dcc.Loading(
                                        id="loading-group-likes-plot",
                                        children=[
                                            dcc.Graph(id="group-likes-plot")
                                        ],
                                        type="default",
                                    )
                                ],
                            ),
                            dcc.Tab(
                                label="Репосты",
                                children=[
                                    dcc.Loading(
                                        id="loading-group-reposts-plot",
                                        children=[
                                            dcc.Graph(id="group-reposts-plot")
                                        ],
                                        type="default",
                                    )
                                ],
                            ),
                        ],
                    )
                ],
                style={'color': 'black'}
            ),
        ])

    @property
    def WordCloudCard(self) -> dbc.Card:
        return dbc.Card([
            dbc.CardHeader(html.H4("Наиболее упоминаемые сущности")),
            dbc.Alert(
                "Недостаточно данных для для отображения графиков",
                id="no-data-alert",
                color="warning",
                style={"display": "none"},
            ),
            dbc.CardBody(
                [
                    dbc.Row(
                        [
                            # dbc.Col(
                            #     dcc.Loading(
                            #         id="loading-frequencies",
                            #         children=[dcc.Graph(id="frequency_figure")],
                            #         type="default",
                            #     )
                            # ),
                            dbc.Col(
                                [
                                    dcc.Tabs(
                                        id="wordcloud-plots",
                                        children=[
                                            dcc.Tab(
                                                label="Древовидная диаграмма слов",
                                                children=[
                                                    dcc.Loading(
                                                        id="loading-treemap",
                                                        children=[dcc.Graph(id="news-treemap")],
                                                        type="default",
                                                    )
                                                ],
                                            ),
                                            dcc.Tab(
                                                label="Облако слов",
                                                children=[
                                                    dcc.Loading(
                                                        id="loading-wordcloud",
                                                        children=[
                                                            dcc.Graph(id="news-wordcloud")
                                                        ],
                                                        type="default",
                                                    )
                                                ],
                                            ),
                                        ],
                                    )
                                ],
                                # md=8,
                            ),
                        ]
                    )
                ],
                style={'color': 'black'}
            ),
        ])
