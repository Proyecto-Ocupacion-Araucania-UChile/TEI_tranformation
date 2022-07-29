from lxml import etree as ET

from .opt.inventory import Inventory
from .teiheader import TreeHeader
from .sourceDoc import SourceDoc

class XML:
    NS = {'alto': "http://www.loc.gov/standards/alto/ns-v4#"}
    tags = None
    root = None
    meta = None

    def __init__(self, name, path):
        self.name = name
        self.path = path
        self.id = "000" + name[:3]
        self.id_archive = "AH0" + name[:3]

    def _preparation_metadada(self):
        from .opt.build_alto import ALTO

        self.tags = ALTO.labels(self)
        self.root = ET.Element("TEI", {"xmlns": "http://www.tei-c.org/ns/1.0", 'xml': 'http://www.w3.org/XML/1998/namespace'})
        data_csv = Inventory(self.name)
        self.meta = data_csv.metadata()

    def building_teiheader(self):
        self._preparation_metadada()
        teiheader = TreeHeader(self.root, meta=self.meta, id_archive=self.id_archive)
        teiheader.build()
        truc = ET.tostring(self.root, encoding='us-ascii', method='xml', xml_declaration=True, pretty_print=True)
        print(truc)

    def building_sourcedesc(self):
        sourcedoc = SourceDoc.sourcedoc(self.path, self.root, self.tags)
        return sourcedoc






