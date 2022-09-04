from lxml import etree as ET
from lxml.etree import _Element


def body(root: _Element, data: list, type_: str):
    """
    Function to build the text element in XML-TEI format with XML-ALTO files and segmonto labelisation

    :param root: Root of etree element
    :param data: List of namedtuple of lines
    :param type_: type of documents
    :return: None
    """
    #Roots
    text = ET.SubElement(root, "text")
    body_root = ET.SubElement(text, "body")
    div = ET.SubElement(body_root, "div", {"type": type_})

    #variable elements and position
    opener = None
    closer = None
    noteGrp = ET.SubElement(text, "noteGrp")
    postscript = None
    ps_note = None
    ps_zone = None
    last_element_closer = None
    commentary = None

    #count paragraph
    n_p = 0

    for line in data:
        # prepare attributes for the text block's zone
        zone_atts = {"corresp": f"#{line.zone_id}"}
        # prepare <lb/> with this line's xml:id as @corresp
        lb = ET.Element("lb", corresp=f"#{line.id}")
        lb.tail = f"{line.text.replace('⁋', '')}"

        # if this is the page's first line, create a <pb> with the page's xml:id
        if int(line.n) == 1:
            pb = ET.Element("pb", corresp=f"#{line.page_id}")
            div.append(pb)

        # find the first and last elements added to the div
        first_element = div[0]
        last_element = div[-1]

        # NumberingZone:page, NumberingZone:other line
        if line.zone_type == "NumberingZone:page" or line.zone_type == "NumberingZone:other":
            # enclose any page number, quire marks, or running title inside a <fw>
            fw = ET.Element("fw", zone_atts)
            if line.zone_type == "NumberingZone:page":
                fw.set("type", "n_page")
            if line.zone_type == "NumberingZone:other":
                fw.set("type", "other_ref")
            last_element.addnext(fw)
            fw.append(lb)

        #CustomZone address line
        elif line.zone_type == "CustomZone:Address":
            #Check if opener exist
            if opener is None:
                opener = ET.Element("opener")
                first_element.addnext(opener)
            name = ET.SubElement(opener, "name", zone_atts)
            name.set("type", "addressee")
            name.append(lb)

        # CustomZone Dateline line
        elif line.zone_type == "CustomZone:Dateline":
            # Check if opener exist
            if opener is None:
                opener = ET.Element("opener")
                first_element.addnext(opener)
            dateline = ET.SubElement(opener, "dateline", zone_atts)
            dateline.append(lb)

        # MainZone SaluteIntro line
        elif line.zone_type == "MainZone:SaluteIntro":
            # Check if opener exist
            if opener is None:
                opener = ET.Element("opener")
                first_element.addnext(opener)
            salute = ET.SubElement(opener, "salute", zone_atts)
            salute.append(lb)

        # StampZone graphic line
        elif line.zone_type == "StampZone:graphic":
            # Check if opener exist
            if opener is None:
                opener = ET.Element("opener")
                first_element.addnext(opener)
            stamp = ET.SubElement(opener, "stamp", zone_atts)
            stamp.set("type", "graphic")
            figure = ET.SubElement(stamp, "figure")
            head = ET.SubElement(figure, "head", corresp=f"#{line.page_id}")
            head.text = line.text
            ET.SubElement(figure, "graphic", url=f"img/{line.page_id}.jpg")
            ET.SubElement(figure, "head")

        # StampZone manuscript line
        elif line.zone_type == "StampZone:manuscript":
            # Check if opener exist
            if opener is None:
                opener = ET.Element("opener")
                first_element.addnext(opener)
            stamp = ET.SubElement(opener, "stamp", zone_atts)
            stamp.set("type", "manuscript")
            name = ET.SubElement(stamp, "name")
            name.append(lb)

        # CustomZone Object line
        elif line.zone_type == "CustomZone:Object":
            head = ET.Element("head")
            first_element.addnext(head, {"head": f"#{line.zone_id}, t"})
            head.append(lb)

        elif line.zone_type == "MainZone:SaluteConclude":
            #Check if closer exist and add first salute
            if closer is None:
                closer = ET.SubElement(div, "closer")
                n_p += 1
                salute = ET.SubElement(closer, "salute", {"corresp": f"#{line.zone_id}", "n": f"{n_p}"})
                # update the last element in closer
                salute.append(lb)
                last_element_closer = closer[-1]
            elif closer is not None and line.text.startswith("⁋"):
                n_p += 1
                salute = ET.Element("salute", {"corresp": f"#{line.zone_id}", "n": f"{n_p}"})
                last_element_closer.addnext(salute)
                # update the last element in closer
                last_element_closer = closer[-1]
                last_element_closer.append(lb)
            # if the line is not emphasized, append it to the last element in the <ab>
            elif line.line_type == "DefaultLine":
                last_element_closer.append(lb)

        elif line.zone_type == "QuireMarksZone:signature":
            if closer is None:
                closer = ET.SubElement(div, "closer")
            signed = ET.SubElement(closer, "signed")
            signed.append(lb)
            last_element_closer = closer[-1]


        # MarginTextZone note
        elif line.zone_type == "MarginTextZone:note":
            #Create element postscript
            if postscript is None:
                postscript = ET.SubElement(div, "postscript")
                ps_note = ET.Element("note")
                postscript.append(ps_note)
                n_p += 1
                ps_zone = line.zone_id
                p = ET.SubElement(ps_note, "p", {"corresp": f"#{line.zone_id}", "n": f"{n_p}"})
                p.append(lb)
            else:
                last_element_postscript = postscript[-1]
                last_element_note = ps_note[-1]
                if ps_zone != line.zone_id:
                    ps_note = ET.Element("note")
                    postscript.append(ps_note)
                    n_p += 1
                    ps_zone = line.zone_id
                    p = ET.SubElement(ps_note, "p", {"corresp": f"#{line.zone_id}", "n": f"{n_p}"})
                    p.append(lb)
                elif line.text.startswith("⁋"):
                    n_p += 1
                    p = ET.Element("p", {"corresp": f"#{line.zone_id}", "n": f"{n_p}"})
                    p.append(lb)
                    last_element_postscript.append(p)
                else:
                    last_element_note.append(lb)

        # NumberingZone id
        elif line.zone_type == "NumberingZone:id":
            # create a <note> if find zone and add in noteGrp
            note = ET.SubElement(noteGrp, "note", zone_atts)
            note.set("type", "id_imp")
            note.set("corresp", f"#{line.id}")
            note.text = line.text

        # MarginTextZone:commentary
        elif line.zone_type == "MarginTextZone:commentary":
            # create a <note> if find zone and add in noteGrp
            if commentary is None:
                commentary = ET.SubElement(noteGrp, "note", zone_atts)
                commentary.set("type", "commentary")
                commentary.append(lb)
            else:
                last_element_noteGrp = commentary[-1]
                last_element_noteGrp.append(lb)

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
            # add classical line
            elif line.line_type == "DefaultLine":
                last_element.append(lb)

