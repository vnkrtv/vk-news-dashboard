from datetime import datetime
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd


def groups_pie_chart(data: pd.DataFrame):
    return html.Div([
        html.H4('Groups', style={'text-align': 'center'}),
        dcc.Graph(
            id='Groups-distribution',
            figure=go.Figure(
                layout=dict(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)'),
                data=[go.Pie(
                    labels=data['groups'],
                    values=data['posts_count'])]
            )
        )
    ])


class LineCharts:

    @staticmethod
    def get_text(row: pd.Series) -> str:
        return str(row)

    @staticmethod
    def views(posts_df: pd.DataFrame, group_screen_name: str): #, start_date: datetime, end_date: datetime) -> html.Div:
        data = posts_df.sort_values(by=['date'], ascending=False)[posts_df['group'] == group_screen_name]
        data['text'] = data.apply(lambda row: '<b>' + row['title'] + '</b><br><br>' +
                                              'Likes: ' + str(row['likes_count']) + '<br>' +
                                              'Comments: ' + str(row['comments_count']) + '<br>' +
                                              'Views: ' + str(row['views_count']) + '<br>' +
                                              'Reposts: ' + str(row['reposts_count']), axis=1)
        return html.Div([
            html.H4('Views for %s' % group_screen_name, style={'text-align': 'center'}),
            dcc.Graph(
                id='views-' + group_screen_name,
                figure=go.Figure(
                    layout=dict(
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)'),
                    data=[go.Scatter(
                        x=data['date'],
                        y=data['views_count'],
                        text=data['text'],
                        hovertemplate='%{text}<br>'
                                      '<extra></extra>'
                    )]
                )
            )
        ])

    @staticmethod
    def likes(posts_df: pd.DataFrame, group_screen_name: str): #, start_date: datetime, end_date: datetime) -> html.Div:
        data = posts_df.sort_values(by=['date'], ascending=False)[posts_df['group'] == group_screen_name]
        data['text'] = data.apply(lambda row: '<b>' + row['title'] + '</b><br><br>' +
                                              'Likes: ' + str(row['likes_count']) + '<br>' +
                                              'Comments: ' + str(row['comments_count']) + '<br>' +
                                              'Views: ' + str(row['views_count']) + '<br>' +
                                              'Reposts: ' + str(row['reposts_count']), axis=1)
        return html.Div([
            html.H4('Likes for %s' % group_screen_name, style={'text-align': 'center'}),
            dcc.Graph(
                id='likes-distribution-' + group_screen_name,
                figure=go.Figure(
                    layout=dict(
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)'),
                    data=[go.Scatter(
                        x=data['date'],
                        y=data['likes_count'],
                        text=data['title'],
                        hovertemplate='%{text}'
                                      '<extra></extra>',
                    )]
                )
            )
        ])

    @staticmethod
    def comments(posts_df: pd.DataFrame, group_screen_name: str): #, start_date: datetime, end_date: datetime) -> html.Div:
        data = posts_df.sort_values(by=['date'], ascending=False)[posts_df['group'] == group_screen_name]
        data['text'] = data.apply(lambda row: '<b>' + row['title'] + '</b><br><br>' +
                                              'Likes: ' + str(row['likes_count']) + '<br>' +
                                              'Comments: ' + str(row['comments_count']) + '<br>' +
                                              'Views: ' + str(row['views_count']) + '<br>' +
                                              'Reposts: ' + str(row['reposts_count']), axis=1)
        return html.Div([
            html.H4('Comments for %s' % group_screen_name, style={'text-align': 'center'}),
            dcc.Graph(
                id='comments-distribution-' + group_screen_name,
                figure=go.Figure(
                    layout=dict(
                        paper_bgcolor='rgba(0,0,0,0)',
                        plot_bgcolor='rgba(0,0,0,0)'),
                    data=[go.Scatter(
                        x=data['date'],
                        y=data['comments_count'],
                        text=data['title'],
                        hovertemplate='%{text}'
                                      '<extra></extra>',
                    )]
                )
            )
        ])