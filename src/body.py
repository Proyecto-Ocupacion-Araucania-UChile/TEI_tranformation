"""from lxml import etree as ET
from collections import namedtuple


class Text:
    root = None

    def __init__(self, root, id_):
        self.root = root
        self.id = id_

    def take_txt(self):
        Line = namedtuple("Line", ["id", "n", "text", "line_type", "zone_type", "zone_id", "page_id"])
        data = [Line(
            ln.getparent().get("{http://www.w3.org/XML/1998/namespace}id"),  # @xml:id of the line's zone
            ln.get("n"),  # line number
            ln.text,  # text content of line
            ln.getparent().get("type"),  # @type of line
            ln.getparent().getparent().get("type"),  # @type of text block zone
            ln.getparent().getparent().get("{http://www.w3.org/XML/1998/namespace}id"),  # @xml:id of text block zone
            ln.getparent().getparent().getparent().get("{http://www.w3.org/XML/1998/namespace}id"),  # @xml:id of page
        ) for ln in self.root.findall('.//line')]
        return data

    @staticmethod
    def build_body(root):
        data = Text.take_txt(Text.root)


        text = ET.SubElement(root, "text")
        body = ET.SubElement(text, "body")
        div = ET.SubElement(body, "div")
        for line in data:
            # prepare attributes for the text block's zone
            zone_atts = {"corresp": f"#{line.zone_id}", "type": line.zone_type}
            # prepare <lb/> with this line's xml:id as @corresp
            lb = ET.Element("lb", corresp=f"#{line.id}")
            lb.tail = f"{line.text}"

            # if this is the page's first line, create a <pb> with the page's xml:id
            if int(line.n) == 1:
                pb = ET.Element("pb", corresp=f"#{line.page_id}")
                div.append(pb)

            # find the last element added to the div
            last_element = div[-1]

            # NumberingZone, QuireMarksZone, and RunningTitleZone line
            if line.zone_type == "NumberingZone" or line.zone_type == "QuireMarksZone" or line.zone_type == "RunningTitleZone":
                # enclose any page number, quire marks, or running title inside a <fw>
                fw = ET.Element("fw", zone_atts)
                last_element.addnext(fw)
                fw.append(lb)

            # MarginTextZone line
            elif line.zone_type == "MarginTextZone":
                # create a <note> if one is not already the preceding sibling
                if last_element.tag != "note":
                    note = ET.Element("note", zone_atts)
                    last_element.addnext(note)
                    note.append(lb)
                else:
                    last_element.append(lb)

            # MainZone line
            elif line.zone_type[:4] == "Main":
                # create an <ab> if one is not already the preceding sibling
                if last_element.tag != "ab":
                    ab = ET.Element("ab", zone_atts)
                    last_element.addnext(ab)
                    # update the last element in div
                    last_element = div[-1]

                # if the line is emphasized for being
                if line.line_type == "DropCapitalLine" or line.line_type == "HeadingLine":
                    # check if there is already an emphasized line in this MainZone
                    ab_children = last_element.getchildren()
                    if len(ab_children) == 0 or ab_children[-1].tag != "hi" or ab_children[-1].get(
                            "rend") != line.line_type:
                        hi = ET.Element("hi", rend=line.line_type)
                        last_element.append(hi)
                        hi.append(lb)
                    elif ab_children[-1].tag == "hi":
                        ab_children[-1].append(lb)

                # if the line is not emphasized, append it to the last element in the <ab>
                elif line.line_type[:7] == "Default":
                    last_element.append(lb)
"""