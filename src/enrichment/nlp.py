import spacy
from lxml import etree as ET
from collections import namedtuple


class NLP:
    Text = None
    GPU = False
    model = "data/models/araucania_NER_model"

    def __init__(self, root, model=None, fishing=True):
        if model is not None:
            self.model = model
        self.fishing = fishing
        self.nlp = self._init_model_()
        self.root = root

    def _init_model_(self):
        self.GPU = spacy.prefer_gpu()
        nlp = spacy.load(self.model)
        if self.fishing is True:
            nlp.add_pipe('entityfishing')
        return nlp

    def __gpu__(self):
        print('GPU:', self.GPU)

    @staticmethod
    def text_compilation() -> list:
        # find all subelement in root (body)
        # return list of nametuple with element and text
        return []

    def preprocessing(self):
        return

    def processing(self):
        return