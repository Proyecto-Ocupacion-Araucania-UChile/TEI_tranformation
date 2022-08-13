from lxml import etree as ET
from datetime import datetime
import numpy as np

from .opt.utils import read_json, date_process
from src.enrichment.sparql import SPARQL


class Index:
    """Class pour post NER to index"""
    NS = {"tei": "http://www.tei-c.org/ns/1.0", "xml": "http://www.w3.org/XML/1998/namespace"}

    def __init__(self, root):
        self.root = root
        ET.register_namespace("xml", Index.NS['xml'])
        self.xml_id = ET.QName(Index.NS['xml'], "id")
        self.xml_base = ET.QName(Index.NS['xml'], "base")
        self.xml_lang = ET.QName(Index.NS['xml'], "lang")
    def build_particDesc(self, elements: list, type_: str):
        for element in elements:
            id_ = element.attrib.get('ref')[1:]
            if type_ == 'PERS':
                xpath = f"//tei:particDesc/tei:listPerson/tei:person[@xml:id ='{id_}']"
                if len(self.root.xpath(xpath, namespaces=Index.NS)) < 1:
                    data = SPARQL.run_sparql(id_)
                    listPerson = self.root.xpath('//tei:particDesc/tei:listPerson', namespaces=Index.NS)
                    if data.sex == np.nan:
                        data.sex = 0
                    person = ET.SubElement(listPerson[0], "person", {self.xml_id: id_, self.xml_base: "https://viaf.org/viaf/"+str(data.id_authority), self.xml_lang: data.language, 'sex': str(data.sex)})
                    persname = ET.SubElement(person, "persname")
                    persname.text = str(data.name)
                    if data.date_birth != np.nan:
                        birth = ET.SubElement(person, "birth", {'when_iso': str(datetime.strptime(data.date_birth, "%d %B %Y"))})
                        birth.text = str(data.date_birth)
                    if data.date_death != np.nan:
                        death = ET.SubElement(person, "death", {'when_iso': str(datetime.strptime(data.date_death, "%d %B %Y"))})
                        death.text = str(data.date_death)
                    if data.description != np.nan:
                        note = ET.SubElement(person, "note", type='description')
                        note.text = str(data.description)
            elif type_ == 'ORG':
                xpath = f"//tei:particDesc/tei:listOrg/tei:org[@xml:id ='{id_}']"
                if len(self.root.xpath(xpath, namespaces=Index.NS)) < 1:
                    data = SPARQL.run_sparql(id_)
                    listOrg = self.root.xpath('//tei:particDesc/tei:listOrg', namespaces=Index.NS)
                    org = ET.SubElement(listOrg[0], "org", {self.xml_id: id_})
                    ET.SubElement(org, "orgname").text = str(data.name)

    def build_settingDesc(self, elements: list):
        for element in elements:
            id_ = element.attrib.get('ref')[1:]
            print(id_)
            xpath = f"//tei:settingDesc/tei:listPlace/tei:place[@xml:id ='{id_}']"
            if len(self.root.xpath(xpath, namespaces=Index.NS)) < 1:
                data = SPARQL.run_sparql(id_)
                listPlace = self.root.xpath('//tei:settingDesc/tei:listPlace', namespaces=Index.NS)
                place = ET.SubElement(listPlace[0], "place", {self.xml_id: id_, self.xml_base: "https://www.geonames.org/"+str(data.id_authority), self.xml_lang: data.language, 'type': str(data.type).replace(" ", "_")})
                ET.SubElement(place, "placename").text = str(data.name)
                if data.region != np.nan:
                    ET.SubElement(place, "region").text = str(data.region)
                if data.country != np.nan:
                    ET.SubElement(place, "country").text = str(data.country)
                if data.loc != np.nan:
                    ET.SubElement(place, "geo").text = str(data.loc)
                if data.description != np.nan:
                    ET.SubElement(place, "note", type='description').text = str(data.description)



class TreeHeader:
    NS_XML = "http://www.w3.org/XML/1998/namespace"
    terms = ["Share — copy and redistribute the material in any medium or format",
             "Adapt — remix, transform, and build upon the material",
             "Attribution — You must give appropriate credit, provide a link to the license, and indicate if changes were made. You may do so in any reasonable manner, but not in any way that suggests the licensor endorses you or your use.",
             "NonCommercial — You may not use the material for commercial purposes.",
             "ShareAlike — If you remix, transform, or build upon the material, you must distribute your contributions under the same license as the original.",
             "The license is restricted to the use of XML-TEI files. The exploitation, distribution or publication of the attached images is subject to the approval of the institution. The full rights of the archive are reserved. The request can be made to the following address: <email>archivo.central@uchile.cl</email>"]

    def __init__(self, root, meta, id_archive):
        self.root = root
        self.author = meta.author
        self.box = meta.box
        self.type_file = meta.type_file
        self.title = meta.title
        self.date = meta.date
        self.loc = meta.loc
        self.nb_page = meta.nb_page
        self.resp = read_json("data/database/resp.json")
        self.id_archive = id_archive

    def build(self):

        #   Base
        teiHeader = ET.SubElement(self.root, "teiHeader")

        # Generate attributs namespace
        ET.register_namespace("xml", TreeHeader.NS_XML)
        ns_id = ET.QName(TreeHeader.NS_XML, "id")
        ns_lang = ET.QName(TreeHeader.NS_XML, "lang")

        # Three children of the root <teiHeader>
        fileDesc = ET.SubElement(teiHeader, "fileDesc")
        profileDesc = ET.SubElement(teiHeader, "profileDesc")
        encodingDesc = ET.SubElement(teiHeader, "encodingDesc")

        # <fileDesc>
        ## titleStmt
        titleStmt = ET.SubElement(fileDesc, "titleStmt")
        ts_title = ET.SubElement(titleStmt, "title")  # pass to other methods
        ts_title.text = self.title
        for i in range(len(self.author)):
            auteur = ET.SubElement(titleStmt, "author")
            auteur.text = self.author[i]
        editor = ET.SubElement(titleStmt, "editor")
        orgName = ET.SubElement(editor, "orgName")
        orgName.text = "Archivo Central Andres Bello"
        ## editionStmt
        editionStmt = ET.SubElement(fileDesc, "editionStmt")
        for i in range(len(self.resp)):
            respStmt = ET.SubElement(editionStmt, "respStmt")
            resp = ET.SubElement(respStmt, "resp")
            resp.text = self.resp[i]["resp"]
            resp.set(ns_id, self.resp[i]["@id"])
            persName = ET.SubElement(respStmt, "persName")
            forename = ET.SubElement(persName, "forename")
            surname = ET.SubElement(persName, "surname")
            forename.text = self.resp[i]["forename"]
            surname.text = self.resp[i]["surname"]
            roleName = ET.SubElement(persName, "roleName")
            roleName.text = self.resp[i]["role"]
            affiliation = ET.SubElement(persName, "affiliation")
            affiliation.text = self.resp[i]["affiliation"]
        ## extent
        extent = ET.SubElement(fileDesc, "extent")
        ET.SubElement(extent, "measure", unit="images", n=str(self.nb_page))
        ## publicationStmt
        publicationStmt = ET.SubElement(fileDesc, "publicationStmt")
        publisher = ET.SubElement(publicationStmt, "publisher")
        publisher.text = "Archivo Central Andres Bello"
        publisher.set(ns_id, "ACAB")
        authority = ET.SubElement(publicationStmt, "authority")
        authority.text = "Área de Información Bibliográfica y Archivística"
        adress = ET.SubElement(publicationStmt, "address")
        ET.SubElement(adress, "country", key="CL")
        region = ET.SubElement(adress, "region")
        region.text = "Región Metropolitana"
        settlement = ET.SubElement(adress, "settlement", type="city")
        settlement.text = "Santiago Centro"
        postCode = ET.SubElement(adress, "postCode")
        postCode.text = "8320000"
        street = ET.SubElement(adress, "street")
        street.text = "Arturo Prat"
        num = ET.SubElement(adress, "street")
        num.text = "#23"
        ### licence
        availability = ET.SubElement(publicationStmt, "availability", status="restricted")
        licence = ET.SubElement(availability, "licence",
                                   target="https://creativecommons.org/licenses/by-sa/3.0/deed.fr")
        licence.text = "Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)"
        for i in range(len(self.terms)):
            auteur = ET.SubElement(availability, "p")
            auteur.text = self.terms[i]
        ### date
        date = ET.SubElement(publicationStmt, "date")
        date.set("when-iso", date_process())

        ## NoteStmt
        notesStmt = ET.SubElement(fileDesc, "notesStmt")
        note1 = ET.SubElement(notesStmt, "note")
        note2 = ET.SubElement(notesStmt, "note")
        note3 = ET.SubElement(notesStmt, "note")
        note1.text = "Digital editing done as part of an international internship."
        note2.text = """A first transcription of part of the collection was made in <date when-iso="2014-06">2014</date> by <persName>Cecilia del Carmen Ramallo Díaz</persName>."""
        note3.text = """HTR scanning done at Universidad de Chile with kraken engine and the application eScriptorium. The HTR models from the transcript are available at this address <ref target="https://github.com/Proyecto-Ocupacion-Araucania-UChile/model-HTR">github</ref>"""

        ## sourceDesc
        sourceDesc = ET.SubElement(fileDesc, "sourceDesc")
        bibl = ET.SubElement(sourceDesc, "bibl")
        series = ET.SubElement(bibl, "series", attrib={ns_lang: "es"})
        title_sp = ET.SubElement(series, "title", attrib={"series": "s", "type": "principal"})
        title_sp.text = "Colección Manuscritos"
        title_sb = ET.SubElement(series, "title", attrib={"type": "subtitle"})
        title_sb.text = "Pacificacion de la Araucania"
        respStmt_s = ET.SubElement(series, "respStmt")
        resp_s = ET.SubElement(respStmt_s, "resp")
        resp_s.text = "Classification and conservation by"
        pers1 = ET.SubElement(respStmt_s, "persName", ref="#DirSc")
        pers1.text = "Alessandro Chiaretti"
        pers2 = ET.SubElement(respStmt_s, "persName", attrib={ns_id: "M_Parra"})
        pers2.text = "Marcos Parra"
        org = ET.SubElement(respStmt_s, "orgName", ref="#ACAB")
        org.text = "Área de Información Bibliográfica y Archivística"
        ET.SubElement(series, "idno", attrib={"type": "caja", "n": self.box})
        ET.SubElement(series, "idno", attrib={"type": "id", "n": self.id_archive})
        note_s = ET.SubElement(series, "note")
        ET.SubElement(note_s, "unit", attrib={"type": "documents", "quantity": "255"})

        # <encodingDesc>
        editorialDecl = ET.SubElement(encodingDesc, "editorialDecl")
        p_edi = ET.SubElement(editorialDecl, "p")
        p_edi.text = "Encoding with XML-TEI P5"
        correction = ET.SubElement(editorialDecl, "correction")
        p_corr = ET.SubElement(correction, "p")
        p_corr.text = "There are no corrections for spelling or grammatical errors. The transcription is as original as possible. A post-process HTR correction was performed via spellchecker and Levenshtein's Distance algorithm."
        punctuation = ET.SubElement(editorialDecl, "punctuation")
        punctuation.text = """<p>The punctuation has been transcribed as found.</p>"""
        segmentation = ET.SubElement(editorialDecl, "segmentation", attrib={"target": "https://github.com/segmonto"})
        segmentation.text = "<p>The segmentation is done via the kraken segmentation model and restructured from the XML-ALTO files and Segmonto ontology.</p>"
        normalization = ET.SubElement(editorialDecl, "normalization")
        normalization.text = """<p>Words that are crossed out, illegible or only interpretable have not been transcribed.</p>"""
        appInfo = ET.SubElement(encodingDesc, "appInfo")
        application1 = ET.SubElement(appInfo, "application", attrib={"version": "4.1.1", "ident": "kraken"})
        label1 = ET.SubElement(application1, "label")
        label1.text = "Kraken HTR"
        ET.SubElement(application1, "ptr", attrib={"target": "https://github.com/mittagessen/kraken"})
        application2 = ET.SubElement(appInfo, "application", attrib={"version": "1.0.0", "ident": "escriptorium"})
        label2 = ET.SubElement(application2, "label")
        label2.text = "eScriptorium"
        ET.SubElement(application2, "ptr", attrib={"target": "https://gitlab.com/scripta/escriptorium"})
        application3 = ET.SubElement(appInfo, "application", attrib={"version": "0.6.3", "ident": "pyspellchecker"})
        label3 = ET.SubElement(application3, "label")
        label3.text = "PYspellchecker"
        ET.SubElement(application3, "ptr", attrib={"target": "https://github.com/barrust/pyspellchecker"})
        application4 = ET.SubElement(appInfo, "application", attrib={"version": "3.4", "ident": "spacy"})
        label4 = ET.SubElement(application4, "label")
        label4.text = "spaCy"
        ET.SubElement(application4, "ptr", attrib={"target": "https://github.com/explosion/spaCy"})

        # profileDesc
        particDesc = ET.SubElement(profileDesc, "particDesc")
        listOrg = ET.SubElement(particDesc, "listOrg")
        head_org = ET.SubElement(listOrg, "head")
        head_org.text = "List of organizations"
        listPerson = ET.SubElement(particDesc, "listPerson")
        head_pers = ET.SubElement(listPerson, "head")
        head_pers.text = "List of persons"
        settingDesc = ET.SubElement(profileDesc, "settingDesc")
        listPlace = ET.SubElement(settingDesc, "listPlace")
        head_loc = ET.SubElement(listPlace, "head")
        head_loc.text ="List of places"
