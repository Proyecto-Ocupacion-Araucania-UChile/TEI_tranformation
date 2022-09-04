from collections import defaultdict
from lxml import etree as ET

class ALTO:
    """
    Subclass to process each unit of the XML-ALTO file group
    """
    NS = {'alto': "http://www.loc.gov/standards/alto/ns-v4#"}

    @staticmethod
    def labels(path):
        """Creates a dictionary of a tag's ID (key) and its LABEL (value).
           The IDs are unique to each document and must be recalculated for each directory.
        """
        root = ET.parse(path).getroot()
        elements = [t.attrib for t in root.findall('.//alto:OtherTag', namespaces=ALTO.NS)]
        collect = defaultdict(dict)
        for d in elements:
            collect[d["ID"]] = d["LABEL"]
        return dict(collect)
