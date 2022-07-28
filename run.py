from collections import namedtuple
from pathlib import Path

from src.build import XML
from src.sourceDoc import SourceDoc


#https://github.com/e-ditiones/Annotator to apply NER

def run():
    p = Path('./data/input/')

    files = []
    Docs = namedtuple("Doc", ["name", "path"])
    for doc in sorted(list(p.glob('*.xml'))):
        files.append(Docs(doc.name, doc))

    td_elem = None

    for file in files:
        xml = XML(file.name, file.path)
        teiHeader = xml.building_teiheader()
        tags = SourceDoc._labels(file.path)
        print(tags)







if __name__ == '__main__':
    run()