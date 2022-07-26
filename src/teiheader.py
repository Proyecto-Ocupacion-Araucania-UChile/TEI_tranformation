from .build import XML
from .opt.inventory import Inventory

class Index:
    """Class pour post NER to index"""
    def build_Pers(self):
        return

    def build_Loc(self):
        return

class GenericDATA(XML):


    def author_data(self, author_element, count):
        """Create and fill datafields for relevant author data.
        Args:
            author_element (etree_Element): <mxc: datafield> being parsed
            count (int): author's count in processing
        Returns:
            data (dict) : relevant authorship data (isni, surname, forename, xml:id)
        """
        # create and set defaults for author data
        fields = ["isni", "primary_name", "secondary_name", "namelink", "xmlid"]
        data = {}
        {data.setdefault(f, None) for f in fields}

        # -- identifier (700s subfield "o") --
        has_isni = author_element.find('m:subfield[@code="o"]', namespaces=NS)
        if has_isni is not None and has_isni.text[0:4] == "ISNI":
            data["isni"] = has_isni.text[4:]

        # -- primary name (700s subfield "a") --
        has_primaryname = author_element.find('m:subfield[@code="a"]', namespaces=NS)
        if has_primaryname is not None:
            data["primary_name"] = has_primaryname.text

        # -- secondary name (700s subfield "b") --
        has_secondaryname = author_element.find('m:subfield[@code="b"]', namespaces=NS)
        if has_secondaryname is not None:
            x = re.search(r"(?:van der)|(?:de la)|(?:de)|(?:du)|(?:von)|(?:van)", has_secondaryname.text)
            if x:
                data["namelink"] = x.group(0)
            y = re.sub(r"(?:van der)|(?:de la)|(?:de)|(?:du)|(?:von)|(?:van)", "", has_secondaryname.text)
            if y != "":
                data["secondary_name"] = y

        # -- unique xml:id for the author --
        if data["primary_name"]:
            name = data["primary_name"]
            data["xmlid"] = f"{name[:2]}{count}"
        elif data["secondary_name"]:
            data["xmlid"] = f"{name[:2]}{count}"
        else:
            data["xmlid"] = f"au{count}"

        return data