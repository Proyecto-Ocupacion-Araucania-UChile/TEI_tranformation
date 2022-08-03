from lxml import etree as ET

from .opt.inventory import Inventory
from .teiheader import TreeHeader

class XML:
    tags = None
    root = None
    meta = None

    def __init__(self, id_, bank_files):
        self.id = id_
        self.bank_files = bank_files
        self.id_archive = "AH0" + id_

    def _preparation_metadada(self):
        self.root = ET.Element("TEI", {"xmlns": "http://www.tei-c.org/ns/1.0", 'xml': 'http://www.w3.org/XML/1998/namespace'})
        data_csv = Inventory(self.id)
        self.meta = data_csv.metadata()

    def building_teiheader(self):
        self._preparation_metadada()
        teiheader = TreeHeader(self.root, meta=self.meta, id_archive=self.id_archive)
        teiheader.build()

    def alto_extraction(self):
        from .opt.extract_alto import ALTO

        for file in self.bank_files:
            alto = ALTO(name=file.name, path=file.path, id_=self.id, bank_files=self.bank_files)
            alto.building_sourcedesc()





