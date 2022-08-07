from lxml import etree as ET


def body(root, data, type_):
    text = ET.SubElement(root, "text")
    body_root = ET.SubElement(text, "body")
    div = ET.SubElement(body_root, "div", {"type": type_})

    opener = None
    closer = None
    noteGrp = ET.SubElement(text, "noteGrp")
    postscript = None
    last_element_closer = None

    n_p = 0

    for line in data:
        # prepare attributes for the text block's zone
        zone_atts = {"corresp": f"#{line.zone_id}"}
        # prepare <lb/> with this line's xml:id as @corresp
        lb = ET.Element("lb", corresp=f"#{line.id}")
        lb.tail = f"{line.text}"

        # if this is the page's first line, create a <pb> with the page's xml:id
        if int(line.n) == 1:
            pb = ET.Element("pb", corresp=f"#{line.page_id}")
            div.append(pb)

        # find the last element added to the div
        first_element = div[0]
        last_element = div[-1]

        # NumberingZone:page, NumberingZone:other line
        if line.zone_type == "NumberingZone:page" or line.zone_type == "NumberingZone:other":
            # enclose any page number, quire marks, or running title inside a <fw>
            fw = ET.Element("fw", zone_atts)
            fw.set("type", "n_page")
            last_element.addnext(fw)
            fw.append(lb)

        if line.zone_type == "CustomZone:Address":
            if opener is None:
                opener = ET.Element("opener")
            first_element.addnext(opener)
            name = ET.SubElement(opener, "name", {"type": "addressee"})
            name.append(lb)

        if line.zone_type == "CustomZone:Dateline":
            if opener is None:
                opener = ET.Element("opener")
            first_element.addnext(opener)
            dateline = ET.SubElement(opener, "dateline")
            dateline.append(lb)

        if line.zone_type == "MainZone:SaluteIntro":
            if opener is None:
                opener = ET.Element("opener")
            first_element.addnext(opener)
            salute = ET.SubElement(opener, "salute")
            salute.append(lb)

        if line.zone_type == "CustomZone:Object":
            head = ET.Element("head")
            first_element.addnext(head, {"head": f"#{line.zone_id}, t"})
            head.append(lb)

        if line.zone_type == "MainZone:SaluteConclude":
            if closer is None:
                closer = ET.SubElement(div, "closer")
                n_p += 1
                p = ET.SubElement(closer, "p", {"corresp": f"#{line.zone_id}", "n": f"{n_p}"})
                # update the last element in div
                p.append(lb)
                last_element_closer = closer[-1]
            elif line.text.startswith("⁋"):
                n_p += 1
                p = ET.Element("p", {"corresp": f"#{line.zone_id}", "n": f"{n_p}"})
                last_element_closer.addnext(p)
                # update the last element in div
                last_element_closer = closer[-1]
                last_element_closer.append(lb)
            # if the line is not emphasized, append it to the last element in the <ab>
            elif line.line_type == "DefaultLine":
                last_element_closer.append(lb)

        # TODO bug des paragraphes
        # MarginTextZone note
        elif line.zone_type == "MarginTextZone:note":
            if postscript is None:
                postscript = ET.SubElement(div, "postscript")
                note = ET.Element("note")
                postscript.append(note)
                n_p += 1
                p = ET.SubElement(note, "p", {"corresp": f"#{line.zone_id}", "n": f"{n_p}"})
                p.append(lb)
            # create a <note> if one is not already the preceding sibling
            else:
                last_element_postscript = postscript[-1]
                if line.text.startswith("⁋"):
                    n_p += 1
                    p = ET.Element("p", {"corresp": f"#{line.zone_id}", "n": f"{n_p}"})
                    last_element_postscript.append(p)
                    # update the last element in div
                    last_element_postscript.append(lb)
                else:
                    last_element_postscript.append(lb)

        # MarginTextZone commentary
        elif line.zone_type == "MarginTextZone:commentary":
            # create a <note> if find zone and add in noteGrp
            note = ET.SubElement(noteGrp, "note", zone_atts)
            note.set("type", "postscript")
            note.text = line.text

        # NumberingZone id
        elif line.zone_type == "NumberingZone:id":
            # create a <note> if find zone and add in noteGrp
            note = ET.SubElement(noteGrp, "note", zone_atts)
            note.set("type", "id_imp")
            note.text = line.text

        # MainZone line
        elif line.zone_type == "MainZone:Text":
            # create an <p> if one is not already the preceding sibling
            if last_element.tag != "p":
                n_p += 1
                p = ET.Element("p", {"corresp": f"#{line.zone_id}", "n": f"{n_p}"})
                last_element.addnext(p)
                # update the last element in div
                last_element = div[-1]
                last_element.append(lb)
            elif line.text.startswith("⁋"):
                n_p += 1
                p = ET.Element("p", {"corresp": f"#{line.zone_id}", "n": f"{n_p}"})
                last_element.addnext(p)
                # update the last element in div
                last_element = div[-1]
                last_element.append(lb)
            # if the line is not emphasized, append it to the last element in the <ab>
            elif line.line_type == "DefaultLine":
                last_element.append(lb)
