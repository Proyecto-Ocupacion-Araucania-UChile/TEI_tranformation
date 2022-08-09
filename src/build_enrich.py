from lxml import etree as ET
from src.enrichment.nlp import NLP
from src.opt.utils import write_xml


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
        file = NLP(self.tree, self.name)
        text = file.plain()
        xml = file.processing_NER(text)
        root = xml.tei_tree.getroot()
        write_xml(path=self.path, root=root)


