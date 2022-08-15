from collections import namedtuple
import pandas as pd
import re


class Text:
    def __init__(self, root):
        self.root = root
        self.data = self.line_data()

    def line_data(self):
        """Parse contextual and attribute data for each text line and store it in a named tuple.
        Returns:
            data (list of named tuples): list of data for each text line
        """
        Line = namedtuple("Line", ["id", "n", "text", "line_type", "zone_type", "zone_id", "page_id", "idAlto"])
        data = []

        for ln in self.root.findall('.//line'):
            # Define type of line
            typeLine = ln.getparent().get("type")
            # Get type
            if ln.getparent().get("subtype") != "none":
                typeLine = typeLine + ":" + ln.getparent().get("subtype"),  # @type of line
            # We retype the strings in tuple
            if type(typeLine) == str:
                typeLine = (typeLine,)
            # Define type of region
            typeRegion = ln.getparent().getparent().get("type")
            # Get it if exist
            if ln.getparent().getparent().get("subtype") != "none":
                typeRegion = typeRegion + ":" + ln.getparent().getparent().get("subtype")
            if type(typeRegion) == str:
                typeRegion = (typeRegion,)

            data.append(
                Line(
                    ln.getparent().get("{http://www.w3.org/XML/1998/namespace}id"),  # @xml:id of the line's zone
                    ln.getparent().get("n"),  # line number
                    ln.text,  # text content of line
                    typeLine[0],
                    typeRegion[0],  # @type of text block zone
                    ln.getparent().getparent().get("{http://www.w3.org/XML/1998/namespace}id"),
                    # @xml:id of text block zone
                    ln.getparent().getparent().getparent().get("{http://www.w3.org/XML/1998/namespace}id"),
                    # @xml:id of page
                    ln.getparent().get("corresp")  # Identifiant de l'élément alto
                )
            )

        return data

    def extract(self):
        """Extract MainZone text lines and clean data by joining broken words and completing abbreviations.
        Returns:
            s (str): text of entire document
        """
        df = pd.DataFrame(self.data)
        # join the text lines and words broken across line breaks together
        s = "%%".join(df.loc[df["zone_type"] == "MainZone"]["text"])
        s = re.sub(r"⁊", "et", s)
        s = re.sub(r"[¬|\-]%%", "", s)
        s = re.sub(r"%%", " ", s)
        # break up the string into segments small enough for the segmentation model
        s = re.sub(r"(\.\s)([A-ZÉÀ])", r"\g<1>\n\g<2>",
                   s)  # capture a period and space (group 1) before capital letter or ⁋ (group 2)
        s = re.sub(r"(?<!\n)Et\s|(?<!\n)⁋", r"\n\g<0>", s)  # capture "Et " if it is not preceded by string beginning
        s = re.sub(r"(?<!\n);|(?<!\n)\?|(?<!\n)\!", r"\g<0>\n", s)  #
        lines = s.split('\n')
        return lines
