from collections import namedtuple, defaultdict
from pathlib import Path
import re

from src.build import XML


#https://github.com/e-ditiones/Annotator to apply NER

def run():
    p = Path('./data/input/')

    files = defaultdict(list)
    Docs = namedtuple("Doc", ["name", "path", "id_group"])
    for doc in sorted(list(p.glob('*.xml'))):
        matching_id = re.match(r"^(\d+)_", doc.name)
        id_ = matching_id.group(1)
        docs = Docs(doc.name, doc, str(id_))
        files[str(id_)].append(docs)


    for file in files:
        xml = XML(file.name, file.path)
        xml.building_teiheader()
        xml.building_sourcedesc()







if __name__ == '__main__':
    run()