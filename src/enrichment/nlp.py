import spacy
from lxml import etree as ET
from collections import namedtuple
from standoffconverter import Standoff, View


#TODO https://github.com/standoff-nlp/standoffconverter/blob/master/examples/named_entities.ipynb
#TODO https://so.davidlassner.com/   c est la demo
#TODO https://e-editiones.org/names-sell-named-entity-recognition-in-tei-publisher/
#TODO https://github.com/eeditiones/tei-publisher-ner
#https://stackoverflow.com/questions/14299978/how-to-use-lxml-to-find-an-element-by-text

class NLP:
    Text = None
    GPU = False
    model = "data/models/araucania_NER_model"

    def __init__(self, tree, model=None, fishing=True):
        if model is not None:
            self.model = model
        self.fishing = fishing
        self.nlp = self._init_model_()
        self.tree = tree
        self.xml_so = Standoff(self.tree, namespaces={"tei": "http://www.tei-c.org/ns/1.0"})
        self.view = self._text_compilation_()

    def _init_model_(self):
        self.GPU = spacy.prefer_gpu()
        nlp = spacy.load(self.model)
        if self.fishing is True:
            nlp.add_pipe("entityfishing")
        return nlp

    def __gpu__(self):
        print('GPU:', self.GPU)

    def _text_compilation_(self) -> View:
        view = (
            View(self.xml_so)
            .shrink_whitespace()
            .insert_tag_text("http://www.tei-c.org/ns/1.0}lb", "\n")
        )
        return view

    def __tokenisation__(self, text):
        return self.nlp(text)

    def plain(self):
        return self.view.get_plain()

    def annotation(self, text):
        doc = self.__tokenisation__(text)
        for ent in doc.ents:
            if ent.label_ == "PERS":
                start_ind = self.view.get_table_pos(ent.start_char)
                end_ind = self.view.get_table_pos(ent.end_char)
                self.xml_so.add_inline(
                    begin=start_ind,
                    end=end_ind,
                    tag="persname",
                    depth=None,
                    attrib={"resp": "spacy"}
                )
                print(ent.text, ent._.kb_qid, ent._.url_wikidata, ent._.nerd_score)
            elif ent.label_ == "ORG":
                start_ind = self.view.get_table_pos(ent.start_char)
                end_ind = self.view.get_table_pos(ent.end_char)
                self.xml_so.add_inline(
                    begin=start_ind,
                    end=end_ind,
                    tag="orgname",
                    depth=None,
                    attrib={"resp": "spacy"}
                )
            elif ent.label_ == "DATE":
                start_ind = self.view.get_table_pos(ent.start_char)
                end_ind = self.view.get_table_pos(ent.end_char)
                self.xml_so.add_inline(
                    begin=start_ind,
                    end=end_ind,
                    tag="date",
                    depth=None,
                    attrib={"resp": "spacy"}
                )
            elif ent.label_ == "LOC":
                start_ind = self.view.get_table_pos(ent.start_char)
                end_ind = self.view.get_table_pos(ent.end_char)
                self.xml_so.add_inline(
                    begin=start_ind,
                    end=end_ind,
                    tag="geoname",
                    depth=None,
                    attrib={"resp": "spacy"}
                )
                #TODO MISC
        return self.xml_so

    def preprocessing(self):
        return

    def processing(self):
        return