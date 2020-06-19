import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd


class LineCharts:

    @staticmethod
    def views(posts_df: pd.DataFrame, group: pd.Series) -> html.Div:
        data = posts_df[posts_df['group'] == group['screen_name']]
        return html.Div([
            html.H4('Просмотры в группе %s' % group['name'], style={'text-align': 'center'}),
            dcc.Graph(
                id='views-' + group['screen_name'],
                figure=go.Figure(
                    layout=dict(
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)'),
                    data=[go.Scatter(
                        x=data['date'],
                        y=data['views_count'],
                        text=data['hovertext'],
                        hovertemplate='%{text}<br>'
                                      '<extra></extra>'
                    )]
                )
            )
        ])

    @staticmethod
    def likes(posts_df: pd.DataFrame, group: pd.Series): #, start_date: datetime, end_date: datetime) -> html.Div:
        data = posts_df[posts_df['group'] == group['screen_name']]
        return html.Div([
            html.H4('Лайки в группе %s' % group['name'], style={'text-align': 'center'}),
            dcc.Graph(
                id='likes-' + group['screen_name'],
                figure=go.Figure(
                    layout=dict(
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)'),
                    data=[go.Scatter(
                        x=data['date'],
                        y=data['likes_count'],
                        text=data['hovertext'],
                        hovertemplate='%{text}'
                                      '<extra></extra>',
                    )]
                )
            )
        ])

    @staticmethod
    def comments(posts_df: pd.DataFrame, group: pd.Series): #, start_date: datetime, end_date: datetime) -> html.Div:
        data = posts_df[posts_df['group'] == group['screen_name']]
        return html.Div([
            html.H4('Комментарии под постами в %s' % group['name'], style={'text-align': 'center'}),
            dcc.Graph(
                id='comments-' + group['screen_name'],
                figure=go.Figure(
                    layout=dict(
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)'),
                    data=[go.Scatter(
                        x=data['date'],
                        y=data['comments_count'],
                        text=data['hovertext'],
                        hovertemplate='%{text}'
                                      '<extra></extra>',
                    )]
                )
            )
        ])