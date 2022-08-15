from lxml import etree as ET

from .opt.inventory import Inventory
from .teiheader import TreeHeader
from .opt.extract_alto import ALTO
from .sourceDoc import SourceDoc
from .opt.utils import write_xml
from .text_data import Text
from .build_body import body


class XML:
    """
    Class to build xml tei base from xml-alto
    """
    tags = None
    root = None
    body = None
    meta = None

    def __init__(self, id_, bank_files):
        """
        initiation class
        :param id_: id of files
        :param bank_files:
        """
        self.id = id_
        self.bank_files = bank_files
        self.id_archive = "AH0" + id_

    def _preparation_metadada(self):
        self.root = ET.Element("TEI",
                               {"xmlns": "http://www.tei-c.org/ns/1.0"})
        data_csv = Inventory(self.id)
        self.meta = data_csv.metadata()

    def building_teiheader(self):
        self._preparation_metadada()
        teiheader = TreeHeader(self.root, meta=self.meta, id_archive=self.id_archive)
        teiheader.build()
        self.tags = ALTO.labels(self.bank_files[0].path)

    def alto_extraction(self):
        sourceDoc = ET.SubElement(self.root, "sourceDoc")
        for file in self.bank_files:
            SourceDoc.sourcedoc_build(file.path, sourceDoc, self.tags)

    def body_creation(self):
        text = Text(self.root)
        body(self.root, text.data, self.meta.type_file)
        write_xml(type=self.meta.type_file, id=self.id, root=self.root)
