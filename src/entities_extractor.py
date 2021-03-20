import datetime
from typing import List, Dict

from natasha import (
    Segmenter,
    MorphVocab,

    NewsEmbedding,
    NewsMorphTagger,
    NewsSyntaxParser,
    NewsNERTagger,

    Doc
)

from src.preprocessing import TextProcessor


class EntitiesExtractor:
    morph_vocab: MorphVocab
    emb: NewsEmbedding
    segmenter: Segmenter
    ner_tagger: NewsNERTagger
    morph_tagger: NewsMorphTagger
    syntax_parser: NewsSyntaxParser

    def __init__(self):
        self.morph_vocab = MorphVocab()
        self.emb = NewsEmbedding()
        self.segmenter = Segmenter()
        self.ner_tagger = NewsNERTagger(self.emb)
        self.morph_tagger = NewsMorphTagger(self.emb)
        self.syntax_parser = NewsSyntaxParser(self.emb)

    def extract_entities(self, text: str) -> List[Dict[str, str]]:
        doc = Doc(text)

        doc.segment(self.segmenter)
        doc.tag_morph(self.morph_tagger)
        doc.parse_syntax(self.syntax_parser)

        doc.tag_ner(self.ner_tagger)
        for span in doc.spans:
            span.normalize(self.morph_vocab)
        entities = [{'text': _.normal, 'type': _.type} for _ in doc.spans]
        return entities

    def get_entities(self, posts_list: List[tuple]) -> List[tuple]:
        entities = []
        posts_df = TextProcessor.parse_posts(posts_list)
        for index, post in posts_df.iterrows():
            post_entities = {}
            for entity in self.extract_entities(post['title']):
                post_entities[entity['text']] = entity['type']
            for entity in self.extract_entities(post['title']):
                post_entities[entity['text']] = entity['type']
            for entity, entity_type in post_entities.items():
                entities.append((post['post_id'], entity_type, post['date'] - datetime.timedelta(hours=3), entity))
        return entities
