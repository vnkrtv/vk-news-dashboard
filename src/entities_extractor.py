import datetime
from typing import List, Dict

from natasha import (
    Segmenter,
    MorphVocab,

    NewsEmbedding,
    NewsMorphTagger,
    NewsSyntaxParser,
    NewsNERTagger,
    NamesExtractor,

    PER,

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
    names_extractor: NamesExtractor

    def __init__(self):
        self.morph_vocab = MorphVocab()
        self.emb = NewsEmbedding()
        self.segmenter = Segmenter()
        self.ner_tagger = NewsNERTagger(self.emb)
        self.morph_tagger = NewsMorphTagger(self.emb)
        self.syntax_parser = NewsSyntaxParser(self.emb)
        self.names_extractor = NamesExtractor(self.morph_vocab)

    def get_doc(self, text: str) -> Doc:
        doc = Doc(text)

        doc.segment(self.segmenter)
        doc.tag_morph(self.morph_tagger)
        doc.parse_syntax(self.syntax_parser)

        doc.tag_ner(self.ner_tagger)
        return doc

    def extract_entities(self, text: str) -> List[Dict[str, str]]:
        doc = self.get_doc(text)
        for span in doc.spans:
            span.normalize(self.morph_vocab)
            if span.type == PER:
                span.extract_fact(self.names_extractor)
        entities = []
        for span in doc.spans:
            if span.type == PER:
                if not span.fact:
                    continue
                facts = span.fact.as_dict
                if 'last' not in facts:
                    continue
                if 'first' in facts:
                    entity = f"{facts['first']} {facts['last']}"
                else:
                    entity = facts['last']
            else:
                entity = span.normal
            entities.append({
                'text': entity,
                'type': span.type
            })
        return entities

    def get_entities(self, posts_list: List[tuple]) -> List[tuple]:
        entities = []
        posts_df = TextProcessor.parse_posts(posts_list)
        for index, post in posts_df.iterrows():
            post_entities = {}
            for entity in self.extract_entities(post['title']):
                post_entities[entity['text']] = entity['type']
            for entity in self.extract_entities(post['text']):
                post_entities[entity['text']] = entity['type']
            for entity, entity_type in post_entities.items():
                entities.append((post['post_id'], entity_type, post['date'] - datetime.timedelta(hours=3), entity))
        return entities
