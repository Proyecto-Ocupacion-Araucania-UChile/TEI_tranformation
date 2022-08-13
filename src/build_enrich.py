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
        Function to apply NER (placename, persname, date) annotation in body root's
        :return: None
        """
        #annotation NER
        file = NLP(self.tree, self.name)
        text = file.plain()
        xml = file.processing_NER(text)
        #get root
        self.root = xml.tei_tree.getroot()
        #Clean variable
        del file, text, xml
        self.tree = None

    def build_profileDesc(self):
        """
        Function to build profileDesc in teiHeader root's
        :return: None
        """
        #TODO remove !!!
        parser = ET.XMLParser(recover=True)
        tree = ET.parse(self.path, parser=parser)
        self.root = tree.getroot()

        #Instance class index
        index = Index(self.root)

        #Get all elements to index
        persname = self.root.xpath('//tei:body/descendant::tei:persname', namespaces=EnrichmentTEI.NS)
        orgname = self.root.xpath('//tei:body/descendant::tei:orgname', namespaces=EnrichmentTEI.NS)
        # TODO change for placename
        geoname = self.root.xpath('//tei:body/descendant::tei:geoname', namespaces=EnrichmentTEI.NS)
        #index.build_particDesc(persname, type_='PERS')
        #index.build_particDesc(orgname, type_='ORG')
        del persname, orgname
        index.build_settingDesc(geoname)
        del geoname

        write_xml(path=self.path, root=self.root)
