import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd


def groups_pie_chart(data: pd.DataFrame):
    graph = html.Div([
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
    return graph