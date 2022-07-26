from pathlib import Path
from collections import namedtuple

import click

from src.build import XML

#https://github.com/e-ditiones/Annotator to apply NER

def run():
    p = Path('./data/input/')

    files = []
    Docs = namedtuple("Doc", ["name", "path"])
    for doc in list(p.glob('*.xml')):
        files.append(Docs(doc.name, doc))

    for file in files:
        xml = XML(file.name, file.path)
        xml.preparation_metadada()
        print(xml.tags)


if __name__ == '__main__':
    run()