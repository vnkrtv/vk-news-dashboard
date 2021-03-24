import re
import datetime
from typing import List

import pandas as pd
import pymorphy2


class TextProcessor:
    morph = pymorphy2.MorphAnalyzer()
    pattern = re.compile(r'\W')
    not_digit = re.compile(r'\D')
    functors_pos = {'INTJ', 'PRCL', 'CONJ', 'PREP'}

    def pos(self, word: str) -> bool:
        return self.morph.parse(word)[0].tag.POS

    def convert(self, text: str) -> str:
        words = [self.pattern.sub('', word) for word in text.split() if self.pos(word) not in self.functors_pos]
        words = [word for word in words if self.not_digit.match(word)]
        words = [self.morph.normal_forms(w)[0] for w in words]
        return ' '.join(words)

    @classmethod
    def parse_title(cls, title: str) -> str:
        if len(title) < 80:
            return title
        processed_title = ''
        one_newline = False
        for i, ch in enumerate(title):
            if 60 < i < 120 and ch == ' ' and not one_newline:
                processed_title += '<br>'
                one_newline = True
            if 120 < i < 180 and ch == ' ' and one_newline:
                processed_title += '<br>'
                one_newline = False
            if 180 < i and ch == ' ' and not one_newline:
                processed_title += '<br>'
                one_newline = True
            else:
                processed_title += ch
        return processed_title

    @classmethod
    def parse_groups(cls, groups_list: List[tuple]) -> pd.DataFrame:
        return pd.DataFrame({
            'group_id': [group[0] for group in groups_list],
            'name': [group[2] for group in groups_list],
            'screen_name': [group[1] for group in groups_list],
            'members_count': [group[3] for group in groups_list]
        })

    @classmethod
    def parse_posts(cls, posts_list: List[tuple]) -> pd.DataFrame:
        df = pd.DataFrame({
            'post_id': [post[0] for post in posts_list],
            'title': [post[3] for post in posts_list],
            'text': [post[4] for post in posts_list],
            'group': [post[1] for post in posts_list],
            'likes_count': [post[5] for post in posts_list],
            'views_count': [post[6] for post in posts_list],
            'comments_count': [post[7] for post in posts_list],
            'reposts_count': [post[8] for post in posts_list],
            'date': [post[2] + datetime.timedelta(hours=3) for post in posts_list]
        })
        df['hovertext'] = df.apply(lambda row: '<b>' + TextProcessor.parse_title(row['title']) + '</b><br><br>' +
                                               'Дата: ' + str(row['date']) + '<br>' +
                                               'Лайки: ' + str(row['likes_count']) + '<br>' +
                                               'Комментарии: ' + str(row['comments_count']) + '<br>' +
                                               'Просмотры: ' + str(row['views_count']) + '<br>' +
                                               'Репосты: ' + str(row['reposts_count']), axis=1)
        return df.sort_values(by=['date'], ascending=False)

    @classmethod
    def parse_entities(cls, entities_list: List[tuple]) -> pd.DataFrame:
        post_ids = []
        types = []
        dates = []
        entities = []
        for entity in entities_list:
            post_ids.append(entity[0])
            types.append(entity[1])
            dates.append(entity[2])
            if entity[1] == 'PER':
                entities.append(entity[3].split()[-1])
            else:
                entities.append(entity[3])
        return pd.DataFrame({
            'post_id': post_ids,
            'type': types,
            'date': dates,
            'entity': entities
        })

    @classmethod
    def process_entities_df(cls, entities_df: pd.DataFrame) -> pd.DataFrame:
        processed_df = entities_df.copy()
        processed_df['entity'] = processed_df.apply(lambda row: row['entity'].split()[-1], axis=1)
        return processed_df
