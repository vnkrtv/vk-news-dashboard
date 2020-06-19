import re
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

    @staticmethod
    def parse_groups(groups_list: list) -> pd.DataFrame:
        return pd.DataFrame({
            'name': [group[2] for group in groups_list],
            'screen_name': [group[1] for group in groups_list],
            'members_count': [group[3] for group in groups_list]
        })

    @staticmethod
    def parse_posts(posts_list: list) -> pd.DataFrame:
        df = pd.DataFrame({
            'title': [post[3] for post in posts_list],
            'text': [post[4] for post in posts_list],
            'group': [post[1] for post in posts_list],
            'likes_count': [post[5] for post in posts_list],
            'views_count': [post[6] for post in posts_list],
            'comments_count': [post[7] for post in posts_list],
            'reposts_count': [post[8] for post in posts_list],
            'date': [post[2] for post in posts_list]
        })
        df['hovertext'] = df.apply(lambda row: '<b>' + row['title'] + '</b><br><br>' +
                                               'Дата: ' + str(row['date']) + '<br>' +
                                               'Лайки: ' + str(row['likes_count']) + '<br>' +
                                               'Комментарии: ' + str(row['comments_count']) + '<br>' +
                                               'Просмотры: ' + str(row['views_count']) + '<br>' +
                                               'Репосты: ' + str(row['reposts_count']), axis=1)
        return df.sort_values(by=['date'], ascending=False)
