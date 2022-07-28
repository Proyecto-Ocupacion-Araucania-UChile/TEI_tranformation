from pathlib import Path
from collections import namedtuple

import click

import numpy as np

from lxml import etree

from src.build import XML

#https://github.com/e-ditiones/Annotator to apply NER

def run():
    p = Path('./data/input/')

    files = []
    Docs = namedtuple("Doc", ["name", "path"])
    for doc in list(p.glob('*.xml')):
        files.append(Docs(doc.name, doc))

    td_elem = None

    for file in files:
        xml = XML(file.name, file.path)
        teiHeader = xml.building_teiheader()

        td_elem = etree.tostring(teiHeader, pretty_print=True, encoding="utf-8")
    print(td_elem)


if __name__ == '__main__':
    run()