from collections import defaultdict
from lxml import etree

from ..build import XML



class ALTO(XML):
    NS = {'alto': "http://www.loc.gov/standards/alto/ns-v4#"}
    
    def __init__(self, name, path, id_):
        super().__init__(id_)
        self.name = name
        self.path = path

    def _labels(self):
        """Creates a dictionary of a tag's ID (key) and its LABEL (value).
           The IDs are unique to each document and must be recalculated for each directory.
        """
        root = etree.parse(self.path).getroot()
        elements = [t.attrib for t in root.findall('.//alto:OtherTag', namespaces=self.NS)]
        collect = defaultdict(dict)
        for d in elements:
            collect[d["ID"]] = d["LABEL"]
        return dict(collect)
