import spacy
from standoffconverter import Standoff, View
from lxml import etree as ET
from src.opt.utils import generate_id, check_csv, journal_error
import pandas as pd
import numpy as np


# TODO https://github.com/standoff-nlp/standoffconverter/blob/master/examples/named_entities.ipynb
# TODO https://so.davidlassner.com/   c est la demo
# TODO https://e-editiones.org/names-sell-named-entity-recognition-in-tei-publisher/
# TODO https://github.com/eeditiones/tei-publisher-ner
# https://stackoverflow.com/questions/14299978/how-to-use-lxml-to-find-an-element-by-text

# Threading
# https://alexandra-zaharia.github.io/posts/how-to-return-a-result-from-a-python-thread/

class NLP:
    NS = {"xmlns": "http://www.tei-c.org/ns/1.0", 'xml': 'http://www.w3.org/XML/1998/namespace'}
    GPU = False
    model = "data/models/araucania_NER_model"
    df_ent = pd.read_csv("data/database/entities.csv", encoding="utf-8")

    def __init__(self, tree, name, model=None, fishing=True):
        if model is not None:
            self.model = model
        self.fishing = fishing
        self.nlp = self._init_model_()
        self.tree = tree
        self.name = name
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

    def processing_NER(self, text):

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
                    attrib=NLP.attribute_NER(ent, self.name)
                )
            elif ent.label_ == "ORG":
                start_ind = self.view.get_table_pos(ent.start_char)
                end_ind = self.view.get_table_pos(ent.end_char)
                self.xml_so.add_inline(
                    begin=start_ind,
                    end=end_ind,
                    tag="orgname",
                    depth=None,
                    attrib=NLP.attribute_NER(ent, self.name)
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
                    attrib=NLP.attribute_NER(ent, self.name)
                )
                # TODO MISC
        NLP.df_ent.to_csv("data/database/entities.csv", encoding="utf-8")
        return self.xml_so

    @staticmethod
    def attribute_NER(ent, file):
        print(ent._.nerd_score)
        df = NLP.df_ent
        # Checker ent
        val_id = check_csv(df, ent._.kb_qid, 'id')
        val_name = check_csv(df, ent.text, 'name')
        # Check if the entity is referenced
        if len(val_id) > 0:
            row = val_id.iloc[0]
            return {"resp": "spacy", "ref": f"#{row.id}"}
        elif len(val_name) > 0:
            row = val_name.iloc[0]
            return {"resp": "spacy", "ref": f"#{row.id}"}
        elif len(val_id) > 0 and len(val_name) > 0:
            # verification of row similarity
            if val_id['id'].iloc[0] == val_name['id'].iloc[0]:
                row = val_id.iloc[0]
                return {"resp": "spacy", "ref": f"#{row.id}"}
            else:
                journal_error(file=file, name=ent.text, error="confusion between entities csv")
        else:
            if ent._.nerd_score is not None and ent._.nerd_score > 0.50:
                new_row = {'id': ent._.kb_qid, 'id_authority': np.nan, 'label_ent': ent.label_, "type": np.nan,
                           "name": ent.text, "names_associated": ent.text, "date_birth": np.nan, "date_end": np.nan,
                           "region": np.nan, "country": np.nan, "description": np.nan, "sex": np.nan,
                           "request": False}
                NLP.df_ent = pd.concat([df, pd.DataFrame([new_row])])
                return {"resp": "spacy", "ref": f"#{ent._.kb_qid}"}
            else:
                id_ = generate_id(ent.label_)
                new_row = {'id': id_, 'id_authority': np.nan, 'label_ent': ent.label_, "type": np.nan,
                           "name": ent.text, "names_associated": ent.text, "date_birth": np.nan, "date_end": np.nan,
                           "region": np.nan, "country": np.nan, "description": np.nan, "sex": np.nan,
                           "request": False}
                NLP.df_ent = pd.concat([df, pd.DataFrame([new_row])])
                return {"resp": "spacy", "ref": f"#{id_}"}
