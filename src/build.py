from lxml import etree as ET

from .opt.inventory import Inventory
from .teiheader import TreeHeader
from .sourceDoc import SourceDoc

from .opt.utils import Tools

class XML:
    tags = None
    root = None
    meta = None

    def __init__(self, id_):
        self.id = id_
        self.id_archive = "AH0" + id_

    def _preparation_metadada(self):
        from .opt.extract_alto import ALTO

        self.tags = ALTO.labels(self)
        self.root = ET.Element("TEI", {"xmlns": "http://www.tei-c.org/ns/1.0", 'xml': 'http://www.w3.org/XML/1998/namespace'})
        data_csv = Inventory(self.id)
        self.meta = data_csv.metadata()

    def building_teiheader(self):
        self._preparation_metadada()
        teiheader = TreeHeader(self.root, meta=self.meta, id_archive=self.id_archive)
        teiheader.build()

    def building_sourcedesc(self):
        SourceDoc.sourcedoc(self.path, self.root, self.tags)
        Tools.write_xml(self.name, self.root)





