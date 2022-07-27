from .opt.inventory import Inventory

from lxml import etree
from lxml.etree import _Element
from collections import namedtuple, defaultdict

from .opt.utils import read_json, date_process


class Index:
    """Class pour post NER to index"""

    def build_Pers(self):
        return

    def build_Loc(self):
        return


class DefaultTree:
    terms = ["Share — copy and redistribute the material in any medium or format",
             "Adapt — remix, transform, and build upon the material",
             "Attribution — You must give appropriate credit, provide a link to the license, and indicate if changes were made. You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.",
             "NonCommercial — You may not use the material for commercial purposes.",
             "ShareAlike — If you remix, transform, or build upon the material, you must distribute your contributions under the same license as the original.",
             "The license is restricted to the use of XML-TEI files. The exploitation, distribution or publication of the attached images is subject to the approval of the institution. The full rights of the archive are reserved. The request can be made to the following address: <email>archivo.central@uchile.cl</email>"]

    def __init__(self, meta, id_archive):
        self.author = meta.author
        self.box = meta.box
        self.type_file = meta.type_file
        self.title = meta.title
        self.date = meta.date
        self.loc = meta.loc
        self.nb_page = meta.nb_page
        self.resp = read_json("data/database/resp.json")
        self.id_archive = id_archive

    def build(self) -> _Element:

        #   Base
        teiHeader = etree.Element("teiHeader")
        # Three children of the root <teiHeader>
        fileDesc = etree.SubElement(teiHeader, "fileDesc")
        profileDesc = etree.SubElement(teiHeader, "profileDesc")
        encodingDesc = etree.SubElement(teiHeader, "encodingDesc")

        # <fileDesc>
        ## titleStmt
        titleStmt = etree.SubElement(fileDesc, "titleStmt")
        ts_title = etree.SubElement(titleStmt, "title")  # pass to other methods
        ts_title.text = self.title
        for i in range(len(self.author)):
            auteur = etree.SubElement(titleStmt, "author")
            auteur.text = self.author[i]
        editor = etree.SubElement(titleStmt, "editor")
        orgName = etree.SubElement(editor, "orgName")
        orgName.text = "Archivo Central Andres Bello"
        ## editionStmt
        editionStmt = etree.SubElement(fileDesc, "editionStmt")
        for i in range(len(self.resp)):
            respStmt = etree.SubElement(editionStmt, "respStmt")
            resp = etree.SubElement(respStmt, "resp")
            resp.text = self.resp[i]["resp"]
            resp.set("xml:id", self.resp[i]["@id"])
            persName = etree.SubElement(respStmt, "persName")
            forename = etree.SubElement(persName, "forename")
            surname = etree.SubElement(persName, "surname")
            forename.text = self.resp[i]["forename"]
            surname.text = self.resp[i]["surname"]
            roleName = etree.SubElement(persName, "roleName")
            roleName.text = self.resp[i]["role"]
            affiliation = etree.SubElement(persName, "affiliation")
            affiliation.text = self.resp[i]["affiliation"]
        ## extent
        extent = etree.SubElement(fileDesc, "extent")
        etree.SubElement(extent, "measure", unit="images", n=self.nb_page)
        ## publicationStmt
        publicationStmt = etree.SubElement(fileDesc, "publicationStmt")
        publisher = etree.SubElement(publicationStmt, "publisher")
        publisher.text = "Archivo Central Andres Bello"
        publisher.set("xml:id", "ACAB")
        authority = etree.SubElement(publicationStmt, "authority")
        authority.text = "Área de Información Bibliográfica y Archivística"
        adress = etree.SubElement(publicationStmt, "address")
        etree.SubElement(adress, "country", key="CL")
        region = etree.SubElement(adress, "address")
        region.text = "Región Metropolitana"
        settlement = etree.SubElement(adress, "settlement", type="city")
        settlement.text = "Santiago Centro"
        postCode = etree.SubElement(adress, "postCode")
        postCode.text = "8320000"
        street = etree.SubElement(adress, "street")
        street.text = "Arturo Prat"
        num = etree.SubElement(adress, "street")
        num.text = "#23"
        ### licence
        availability = etree.SubElement(publicationStmt, "availability", status="restricted")
        licence = etree.SubElement(availability, "licence",
                                   target="https://creativecommons.org/licenses/by-sa/3.0/deed.fr")
        licence.text = "Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)"
        for i in range(len(self.terms)):
            auteur = etree.SubElement(availability, "p")
            auteur.text = self.terms[i]
        ### date
        date = etree.SubElement(publicationStmt, "date")
        date.set("when-iso", date_process())

        ## NoteStmt
        notesStmt = etree.SubElement(fileDesc, "notesStmt")
        note1 = etree.SubElement(notesStmt, "note")
        note2 = etree.SubElement(notesStmt, "note")
        note3 = etree.SubElement(notesStmt, "note")
        note1.text = "Digital editing done as part of an international internship."
        note2.text = """A first transcription of part of the collection was made in <date when-iso="2014-06">2014</date> by <persName>Cecilia del Carmen Ramallo Díaz</persName>."""
        note3.text = """HTR scanning done at Universidad de Chile with kraken engine and the application eScriptorium. The HTR models from the transcript are available at this address <ref target="https://github.com/Proyecto-Ocupacion-Araucania-UChile/model-HTR">github</ref>"""

        ## sourceDesc
        sourceDesc = etree.SubElement(fileDesc, "sourceDesc")
        bibl = etree.SubElement(sourceDesc, "bibl")
        series = etree.SubElement(bibl, "series", attrib={"xml:lang": "es"})
        title_sp = etree.SubElement(series, "title", attrib={"series": "s", "type": "principal"})
        title_sp.text = "Colección Manuscritos"
        title_sb = etree.SubElement(series, "title", attrib={"type": "subtitle"})
        title_sb.text = "Pacificacion de la Araucania"
        respStmt_s = etree.SubElement(series, "respStmt")
        resp_s = etree.SubElement(respStmt_s, "resp")
        resp_s.text = "Classification and conservation by"
        pers1 = etree.SubElement(respStmt_s, "persName", ref="#DirSc")
        pers1.text = "Alessandro Chiaretti"
        pers2 = etree.SubElement(respStmt_s, "persName", attrib={"xml:id": "M_Parra"})
        pers2.text = "Marcos Parra"
        org = etree.SubElement(respStmt_s, "orgName", ref="#ACAB")
        org.text = "Área de Información Bibliográfica y Archivística"
        etree.SubElement(series, "idno", attrib={"type": "caja", "n": self.box})
        etree.SubElement(series, "idno", attrib={"type": "id", "n": self.id_archive})
        note_s = etree.SubElement(series, "note")
        etree.SubElement(note_s, "unit", attrib={"type": "documents", "quantity": "255"})

        # <encodingDesc>
        editorialDecl = etree.SubElement(encodingDesc, "editorialDecl")
        p_edi = etree.SubElement(editorialDecl, "p")
        p_edi.text = "Encoding with XML-TEI P5"
        correction = etree.SubElement(editorialDecl, "correction")
        p_corr = etree.SubElement(correction, "p")
        p_corr.text = "There are no corrections for spelling or grammatical errors. The transcription is as original as possible. A post-process HTR correction was performed via spellchecker and Levenshtein's Distance algorithm."
        punctuation = etree.SubElement(editorialDecl, "punctuation")
        punctuation.text = """<p>The punctuation has been transcribed as found.</p>"""
        segmentation = etree.SubElement(editorialDecl, "segmentation", attrib={"target": "https://github.com/segmonto"})
        segmentation.text = "<p>The segmentation is done via the kraken segmentation model and restructured from the XML-ALTO files and Segmonto ontology.</p>"
        normalization = etree.SubElement(editorialDecl, "normalization")
        normalization.text = """<p>Words that are crossed out, illegible or only interpretable have not been transcribed.</p>"""
        appInfo = etree.SubElement(encodingDesc, "appInfo")
        application1 = etree.SubElement(appInfo, "application", attrib={"version": "4.1.1", "ident": "kraken"})
        label1 = etree.SubElement(application1, "label")
        label1.text = "Kraken HTR"
        etree.SubElement(application1, "ptr", attrib={"target": "https://github.com/mittagessen/kraken"})
        application2 = etree.SubElement(appInfo, "application", attrib={"version": "1.0.0", "ident": "escriptorium"})
        label2 = etree.SubElement(application2, "label")
        label2.text = "eScriptorium"
        etree.SubElement(application2, "ptr", attrib={"target": "https://gitlab.com/scripta/escriptorium"})
        application3 = etree.SubElement(appInfo, "application", attrib={"version": "0.6.3", "ident": "pyspellchecker"})
        label3 = etree.SubElement(application3, "label")
        label3.text = "PYspellchecker"
        etree.SubElement(application3, "ptr", attrib={"target": "https://github.com/barrust/pyspellchecker"})
        application4 = etree.SubElement(appInfo, "application", attrib={"version": "3.4", "ident": "spacy"})
        label4 = etree.SubElement(application4, "label")
        label4.text = "spaCy"
        etree.SubElement(application4, "ptr", attrib={"target": "https://github.com/explosion/spaCy"})

        # profileDesc
        etree.SubElement(profileDesc, "particDesc")
        etree.SubElement(profileDesc, "settingDesc")

        return teiHeader
