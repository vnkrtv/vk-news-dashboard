import datetime
from typing import List, Any

import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import pandas as pd


class LineCharts:

    @staticmethod
    def get_graph(data: pd.DataFrame, title: str, graph_id: str, y_data: str) -> dbc.Card:
        fig = go.Figure(
            layout=dict(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)',),
            data=[go.Scatter(
                x=data['date'],
                y=data[y_data],
                text=data['hovertext'],
                hovertemplate='%{text}<br>'
                              '<extra></extra>'
            )]
        )
        fig.layout.xaxis.range = pd.date_range(
            start=datetime.datetime.now() - datetime.timedelta(days=1),
            end=datetime.datetime.now())
        return dbc.Card([
            html.H4(title, style={'text-align': 'center'}),
            dcc.Graph(
                id=graph_id,
                figure=fig
            )
        ],
            style={'margin-bottom': '3vh'})

    @staticmethod
    def views(posts_df: pd.DataFrame, group: pd.Series) -> html.Div:
        data = posts_df[posts_df['group'] == group['screen_name']]
        return LineCharts.get_graph(data=data,
                                    title='Просмотры в группе %s' % group['name'],
                                    graph_id='views-' + group['screen_name'],
                                    y_data='views_count')

    @staticmethod
    def likes(posts_df: pd.DataFrame, group: pd.Series) -> html.Div:
        data = posts_df[posts_df['group'] == group['screen_name']]
        return LineCharts.get_graph(data=data,
                                    title='Лайки в группе %s' % group['name'],
                                    graph_id='likes-' + group['screen_name'],
                                    y_data='likes_count')

    @staticmethod
    def comments(posts_df: pd.DataFrame, group: pd.Series) -> html.Div:
        data = posts_df[posts_df['group'] == group['screen_name']]
        return LineCharts.get_graph(data=data,
                                    title='Комментарии в группе %s' % group['name'],
                                    graph_id='comments-' + group['screen_name'],
                                    y_data='comments_count')

    @staticmethod
    def reposts(posts_df: pd.DataFrame, group: pd.Series) -> html.Div:
        data = posts_df[posts_df['group'] == group['screen_name']]
        return LineCharts.get_graph(data=data,
                                    title='Репосты в группе %s' % group['name'],
                                    graph_id='reposts-' + group['screen_name'],
                                    y_data='reposts_count')


class NewsTable:

    @staticmethod
    def get_post_href(group_screen_name: str, group_id: int, post_id: int) -> str:
        return f'https://vk.com/{group_screen_name}?w=wall-{group_id}_{post_id}'


    @staticmethod
    def update_news(posts_df: pd.DataFrame, groups_df: pd.DataFrame) -> List[Any]:
        max_rows = 6
        return [
            html.H4(children="Новости"),
            html.P(
                children="Последнее обновление: "
                         + datetime.datetime.now().strftime("%H:%M:%S"),
            ),
            html.Table(
                className="table",
                children=[
                    html.Tr(
                        children=[
                            html.Td(
                                children=[
                                    html.A(
                                        children=posts_df.iloc[i]["title"],
                                        href=NewsTable.get_post_href(
                                            group_screen_name=posts_df.iloc[i]["group"],
                                            post_id=posts_df.iloc[i]["id"],
                                            group_id=groups_df[
                                                groups_df['screen_name'] == posts_df.iloc[i]["group"]
                                            ].iloc[0]['id']),
                                        title=groups_df[
                                            groups_df['screen_name'] == posts_df.iloc[i]["group"]
                                            ].iloc[0]['name'] + '\n' +
                                        str(posts_df.iloc[i]["date"]),
                                        target="_blank",
                                    )
                                ]
                            )
                        ]
                    )
                    for i in range(min(len(posts_df), max_rows))
                ],
            ),
        ]
