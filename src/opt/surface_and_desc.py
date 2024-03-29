from lxml import etree
import re


class SurfaceTree:
    NS = {'a': "http://www.loc.gov/standards/alto/ns-v4#"}
    """Creates a <surface> element and its children for one page (ALTO file) of a document.
    """

    def __init__(self, doc, folio, alto_root):
        self.doc = doc
        self.folio = folio
        self.root = alto_root

    def surface(self, surface_group, page_attributes):
        # -- surfaceGrp/surface--
        # On transforme le chemin de fichier en label
        label = self.folio
        label = label.split('/')[2].replace('.jpg', '')
        surface = etree.SubElement(surface_group, "surface", page_attributes)
        # create <graphic> and assign its attributes
        etree.SubElement(surface, "graphic", url=self.folio)
        return surface

    def zone1(self, surface, textblock_atts, textblock_count):
        # -- surfaceGrp/surface/zone --
        # On transforme le chemin de fichier en label
        label = self.folio
        label = label.split('/')[2].replace('.jpg', '')
        xml_id = {"{http://www.w3.org/XML/1998/namespace}id": f"{label}_z{textblock_count + 1}"}
        text_block = etree.SubElement(surface, "zone", xml_id)
        for k, v in textblock_atts[textblock_count].items():
            text_block.attrib[k] = v
        return text_block

    def zone2(self, lines_on_page, text_block, textblock_count, textline_atts, textline_count, processed_textline):
        # -- surfaceGrp/surface/zone/zone --
        # On transforme le chemin de fichier en label
        label = self.folio
        label = label.split('/')[2].replace('.jpg', '')
        zone_id = {"{http://www.w3.org/XML/1998/namespace}id": f"{label}_z{textblock_count + 1}_l{textline_count + 1}"}
        text_line = etree.SubElement(text_block, "zone", zone_id)
        for k, v in textline_atts[textline_count].items():
            text_line.attrib[k] = v
        text_line.attrib["n"] = str(lines_on_page)
        # -- surfaceGrp/surface/zone/zone --
        # On transforme le chemin de fichier en label
        label = self.folio
        label = label.split('/')[2].replace('.jpg', '')
        path_id = {
            "{http://www.w3.org/XML/1998/namespace}id": f"{label}_z{textblock_count + 1}_l{textline_count + 1}_p"}
        baseline = etree.SubElement(text_line, "path", path_id)
        b = self.root.find(f'.//a:TextLine[@ID="{processed_textline}"]', namespaces=self.NS).get("BASELINE")
        baseline.attrib["points"] = " ".join([re.sub(r"\s", ",", x) for x in re.findall(r"(\d+ \d+)", b)])
        return text_line

    def line(self, text_line, textblock_count, textline_count, processed_textline):
        # -- surfaceGrp/surface/zone/zone/line --
        # On transforme le chemin de fichier en label
        label = self.folio
        label = label.split('/')[2].replace('.jpg', '')
        xml_id = {"{http://www.w3.org/XML/1998/namespace}id": f"{label}_z{textblock_count + 1}_l{textline_count + 1}_t"}
        string = etree.SubElement(text_line, "line", xml_id)
        string.text = self.root.find(f'.//a:TextLine[@ID="{processed_textline}"]/a:String', namespaces=self.NS).get(
            "CONTENT")
        return string