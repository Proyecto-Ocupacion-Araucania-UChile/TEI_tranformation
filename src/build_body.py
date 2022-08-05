from lxml import etree as ET


def body(root, data, type_):
    text = ET.SubElement(root, "text")
    body_root = ET.SubElement(text, "body")
    div = ET.SubElement(body_root, "div", {"type": type_})
    noteGrp = ET.SubElement(text, "noteGrp")

    postscript = None

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

        # MarginTextZone note
        elif line.zone_type == "MarginTextZone:note":
            if postscript is None:
                postscript = ET.SubElement(div, "postscript")
                note = ET.Element("note", zone_atts)
                postscript.append(note)
                note.append(lb)
                last_element_postscript = postscript[-1]
            # create a <note> if one is not already the preceding sibling
            if last_element_postscript.tag != "note":
                note = ET.Element("note", zone_atts)
                last_element_postscript.addnext(note)
                last_element_postscript = postscript[-1]
                note.append(lb)
            elif line.text.startswith("⁋"):
                p = ET.Element("p", zone_atts)
                last_element_postscript.addnext(p)
                # update the last element in div
                last_element_postscript = postscript[-1]
                last_element_postscript.append(lb)
            else:
                last_element_postscript.append(lb)

        # MarginTextZone commentary
        elif line.zone_type == "MarginTextZone:commentary":
            # create a <note> if one is not already the preceding sibling
            if last_element.tag != "note":
                note = ET.Element("note", zone_atts)
                last_element.addnext(note)
                note.append(lb)
            else:
                last_element.append(lb)

        # MainZone line
        elif line.zone_type == "MainZone:Text":
            # create an <p> if one is not already the preceding sibling
            if last_element.tag != "p":
                p = ET.Element("p", zone_atts)
                last_element.addnext(p)
                # update the last element in div
                last_element = div[-1]
                last_element.append(lb)
            elif line.text.startswith("⁋"):
                p = ET.Element("p", zone_atts)
                last_element.addnext(p)
                # update the last element in div
                last_element = div[-1]
                last_element.append(lb)
            # if the line is not emphasized, append it to the last element in the <ab>
            elif line.line_type == "DefaultLine":
                last_element.append(lb)
