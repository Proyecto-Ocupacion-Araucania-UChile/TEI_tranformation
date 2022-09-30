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
        """
        Function to parse xml file
        :return: lxml.etree
        """
        parser = ET.XMLParser(recover=True)
        parsed_file = ET.parse(self.path, parser=parser)
        return parsed_file

    def annotation_NER(self):
        """
        Function to apply NER (placeName, persName, date) annotation in body root's
        :return: None
        """
        # annotation NER
        file = NLP(self.tree, self.name)
        text = file.plain()
        xml = file.processing_NER(text)
        # get root
        self.root = xml.tei_tree.getroot()
        # Clean variable
        del file, text, xml
        self.tree = None

    def build_profileDesc(self):
        """
        Function to build profileDesc in teiHeader root's
        :return: None
        """

        # Instance class index
        index = Index(self.root)

        # Get all elements to index
        persName = self.root.xpath('//tei:body/descendant::persName', namespaces=EnrichmentTEI.NS)
        orgName = self.root.xpath('//tei:body/descendant::orgName', namespaces=EnrichmentTEI.NS)
        placeName = self.root.xpath('//tei:body/descendant::placeName', namespaces=EnrichmentTEI.NS)
        # Build particDesc
        index.build_particDesc(persName, type_='PERS')
        index.build_particDesc(orgName, type_='ORG')
        del persName, orgName
        # Build settingDesc
        index.build_settingDesc(placeName)
        del placeName
        # write final xml
        write_xml(path=self.path, root=self.root)
