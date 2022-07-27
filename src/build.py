from lxml import etree

from .opt.inventory import Inventory
from .teiheader import DefaultTree


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
        self.root = etree.Element("TEI", {"xmlns": "http://www.tei-c.org/ns/1.0"})
        data_csv = Inventory(self.name)
        self.meta = data_csv.metadata()

    def building_teiheader(self):
        self._preparation_metadada()
        teiheader = DefaultTree(meta=self.meta, id_archive=self.id_archive)
        teiheader_build = teiheader.build()



