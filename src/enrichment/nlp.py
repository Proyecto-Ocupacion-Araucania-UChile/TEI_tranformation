import spacy
from lxml import etree as ET
from collections import namedtuple


class NLP:
    Text = None
    GPU = False
    model = "data/models/araucania_NER_model"

    def __init__(self, root, model=None):
        if model is not None:
            self.model = model
        self.nlp = self._init_model_()
        self.root = root

    def _init_model_(self):
        self.GPU = spacy.prefer_gpu()
        return spacy.load(self.model)

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