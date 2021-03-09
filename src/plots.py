import datetime
from typing import List, Any

import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import plotly.graph_objs as go
import pandas as pd
from wordcloud import WordCloud


class LineCharts:

    @staticmethod
    def get_plot(data: pd.DataFrame, y_data: str) -> go.Figure:
        fig = go.Figure(
            layout=dict(
                paper_bgcolor='rgba(0,0,0,0)',
                plot_bgcolor='rgba(0,0,0,0)', ),
            data=[go.Scatter(
                x=data['date'],
                y=data[y_data],
                text=data['hovertext'],
                textfont=dict(color='white'),
                hovertemplate='%{text}<br>'
                              '<extra></extra>'
            )]
        )
        fig.layout.xaxis.range = pd.date_range(
            start=datetime.datetime.now() - datetime.timedelta(days=1),
            end=datetime.datetime.now())
        return fig

    @staticmethod
    def views(data: pd.DataFrame) -> go.Figure:
        return LineCharts.get_plot(data=data, y_data='views_count')

    @staticmethod
    def likes(data: pd.DataFrame) -> go.Figure:
        return LineCharts.get_plot(data=data, y_data='likes_count')

    @staticmethod
    def comments(data: pd.DataFrame) -> go.Figure:
        return LineCharts.get_plot(data=data, y_data='comments_count')

    @staticmethod
    def reposts(data: pd.DataFrame) -> go.Figure:
        return LineCharts.get_plot(data=data, y_data='reposts_count')


class NewsTable:

    @staticmethod
    def get_post_href(group_screen_name: str, group_id: int, post_id: int) -> str:
        return f'https://vk.com/{group_screen_name}?w=wall-{group_id}_{post_id}'

    @staticmethod
    def update_news(posts_df: pd.DataFrame, groups_df: pd.DataFrame) -> List[Any]:
        max_rows = 6
        return [
            dbc.CardHeader(html.H4(children="Новости")),
            dbc.CardBody([
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
                                                post_id=posts_df.iloc[i]["post_id"],
                                                group_id=groups_df[
                                                    groups_df['screen_name'] == posts_df.iloc[i]["group"]
                                                    ].iloc[0]['group_id']),
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
            ])
        ]


class WordCloudPlots:
    stopwords = ['TJ', 'РИА', 'Новости', 'Медуза', 'РБК', 'Pro', 'СМИ', 'Тренд']

    @classmethod
    def get_plots(cls, data: pd.DataFrame) -> Any:
        complaints_text = list(data["entity"].dropna().values)

        if len(complaints_text) < 1:
            return {}, {}, {}

        text = " ".join(complaints_text)

        word_cloud = WordCloud(stopwords=set(cls.stopwords), max_words=100, max_font_size=90)
        word_cloud.generate(text)

        word_list = []
        freq_list = []
        fontsize_list = []
        position_list = []
        orientation_list = []
        color_list = []

        for (word, freq), fontsize, position, orientation, color in word_cloud.layout_:
            word_list.append(word)
            freq_list.append(freq)
            fontsize_list.append(fontsize)
            position_list.append(position)
            orientation_list.append(orientation)
            color_list.append(color)

        # get the positions
        x_arr = []
        y_arr = []
        for i in position_list:
            x_arr.append(i[0])
            y_arr.append(i[1])

        # get the relative occurence frequencies
        new_freq_list = []
        for i in freq_list:
            new_freq_list.append(i * 80)

        new_freq_list = [freq for freq in filter(lambda f: f > 1, new_freq_list)]
        color_list = color_list[:len(new_freq_list)]
        word_list = word_list[:len(new_freq_list)]
        freq_list = freq_list[:len(new_freq_list)]

        trace = go.Scatter(
            x=x_arr,
            y=y_arr,
            textfont=dict(size=new_freq_list, color=color_list),
            hoverinfo="text",
            textposition="top center",
            hovertext=["{0} - {1}".format(w, f) for w, f in zip(word_list, freq_list)],
            mode="text",
            text=word_list,
        )

        layout = go.Layout(
            {
                "paper_bgcolor": 'rgba(0,0,0,0)',
                "plot_bgcolor": 'rgba(0,0,0,0)',
                "xaxis": {
                    "showgrid": False,
                    "showticklabels": False,
                    "zeroline": False,
                    "automargin": True,
                    "range": [-100, 250],
                },
                "yaxis": {
                    "showgrid": False,
                    "showticklabels": False,
                    "zeroline": False,
                    "automargin": True,
                    "range": [-100, 450],
                },
                # "margin": dict(t=20, b=20, l=10, r=10, pad=4),
                "margin": dict(t=10, b=10, l=5, r=5, pad=4),
                "hovermode": "closest",
            }
        )

        wordcloud_figure_data = {"data": [trace], "layout": layout}
        word_list_top = word_list[:25]
        word_list_top.reverse()
        freq_list_top = freq_list[:25]
        freq_list_top.reverse()

        frequency_figure_data = {
            "data": [
                {
                    "y": word_list_top,
                    "x": freq_list_top,
                    "type": "bar",
                    "name": "",
                    "orientation": "h",
                }
            ],
            "layout": {
                "paper_bgcolor": 'rgba(0,0,0,0)',
                "plot_bgcolor": 'rgba(0,0,0,0)',
                'color': 'white',
                "height": "550",
                "margin": dict(t=20, b=20, l=100, r=20, pad=4)
            },
        }
        treemap_trace = go.Treemap(
            labels=word_list_top, parents=[""] * len(word_list_top), values=freq_list_top
        )
        treemap_layout = go.Layout(
            {
                "paper_bgcolor": 'rgba(0,0,0,0)',
                "plot_bgcolor": 'rgba(0,0,0,0)',
                "margin": dict(t=10, b=10, l=5, r=5, pad=4)
            }
        )
        treemap_figure = {"data": [treemap_trace], "layout": treemap_layout}
        return wordcloud_figure_data, frequency_figure_data, treemap_figure
