from collections import defaultdict
from lxml import etree as ET

from ..sourceDoc import SourceDoc

class ALTO:
    """
    Subclass to process each unit of the XML-ALTO file group
    """
    NS = {'alto': "http://www.loc.gov/standards/alto/ns-v4#"}

    @staticmethod
    def labels(path):
        """Creates a dictionary of a tag's ID (key) and its LABEL (value).
           The IDs are unique to each document and must be recalculated for each directory.
        """
        root = ET.parse(path).getroot()
        elements = [t.attrib for t in root.findall('.//alto:OtherTag', namespaces=ALTO.NS)]
        collect = defaultdict(dict)
        for d in elements:
            collect[d["ID"]] = d["LABEL"]
        return dict(collect)

    def body(root, data):
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
            elif line.zone_type == "MainZone":
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
                    if len(ab_children) == 0 or ab_children[-1].tag != "hi":
                        hi = ET.Element("hi", rend=line.line_type)
                        last_element.append(hi)
                        hi.append(lb)
                    elif ab_children[-1].tag == "hi":
                        ab_children[-1].append(lb)

                # if the line is not emphasized, append it to the last element in the <ab>
                elif line.line_type == "DefaultLine":
                    last_element.append(lb)