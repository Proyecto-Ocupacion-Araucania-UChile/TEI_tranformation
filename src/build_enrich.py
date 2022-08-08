from lxml import etree as ET
from src.enrichment.nlp import NLP


class EnrichmentTEI:
    NS = {"xmlns": "http://www.tei-c.org/ns/1.0", 'xml': 'http://www.w3.org/XML/1998/namespace'}

    def __init__(self, name, path):
        self.name = name
        self.path = path
        self.tree = self.__etree__()

    def __etree__(self):
        parser = ET.XMLParser(recover=True)
        parsed_file = ET.parse(self.path, parser=parser)
        return parsed_file

    def annotation_NER(self):
        file = NLP(self.tree)
        text = file.plain()
        new_xml = file.annotation(text)
        xml = ET.tostring(new_xml.tei_tree).decode("utf-8")
        print(xml)


