import spacy


class NLP:
    Text = None

    def __init__(self, model):
        self.model = model
        self.nlp = self._init_model_()

    def _init_model_(self):
        spacy.prefer_gpu()
        return spacy.load(self.model)

    def

    def preprocessing(self):
        return

    def processing(self):