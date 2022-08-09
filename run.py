from collections import namedtuple, defaultdict
from pathlib import Path
import re
import click

from src.build_tei import XML
from src.build_enrich import EnrichmentTEI


# https://github.com/e-ditiones/Annotator to apply NER voir aussi hugoscheitaeur
# see https://stackoverflow.com/questions/5395948/incredibly-basic-lxml-questions-getting-html-string-content-of-lxml-etree-elem

@click.command()
@click.option("-e", "--enrich", "enrich", is_flag=True, show_default=True, default=False,
              help="Argument for automatic data enrichment")
def run(enrich):
    p_input = Path('./data/input/')
    p_output = Path('./data/output/')

    files = defaultdict(list)
    Docs = namedtuple("Doc", ["name", "path", "id_group"])
    for doc in sorted(list(p_input.glob('*.xml'))):
        matching_id = re.match(r"^(\d+)_", doc.name)
        id_ = matching_id.group(1)
        docs = Docs(doc.name, doc, str(id_))
        files[str(id_)].append(docs)

    # Building teiheader, sourcedoc and body
    for id_group in dict(files):
        xml = XML(str(id_group), files[id_group])
        xml.building_teiheader()
        xml.alto_extraction()
        xml.body_creation()

    # Enrichment of output files
    if enrich:
        # list of files
        Docs_output = namedtuple("Doc", ["name", "path"])
        files_tei = []
        for doc in list(p_output.glob('*.xml')):
            files_tei.append(Docs_output(doc.name, doc))

        for doc in files_tei:
            xml_op = EnrichmentTEI(doc.name, doc.path)
            xml_op.annotation_NER()


if __name__ == '__main__':
    run()
