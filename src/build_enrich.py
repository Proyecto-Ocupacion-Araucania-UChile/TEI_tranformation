from lxml import etree as ET
from src.enrichment.nlp import NLP
from src.opt.utils import write_xml

from src.teiheader import Index


class EnrichmentTEI:
    NS = {"tei": "http://www.tei-c.org/ns/1.0"}

    def __init__(self, name, path):
        self.root = None
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
        self.root = xml.tei_tree.getroot()

    def build_profileDesc(self):
        #TODO remove !!!
        parser = ET.XMLParser(recover=True)
        tree = ET.parse(self.path, parser=parser)
        self.root = tree.getroot()

        #Instance class index
        index = Index(self.root)

        #Get all elements to index
        persname = self.root.xpath('//tei:body/descendant::tei:persname', namespaces=EnrichmentTEI.NS)
        orgname = self.root.xpath('//tei:body/descendant::tei:orgname', namespaces=EnrichmentTEI.NS)
        geoname = self.root.xpath('//tei:body/descendant::tei:geoname', namespaces=EnrichmentTEI.NS)
        #print(geoname[0].attrib.get('{http://www.w3.org/XML/1998/namespace}id'))
        index.build_particDesc(persname)

        #write_xml(path=self.path, root=self.root)
