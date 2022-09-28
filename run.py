from collections import namedtuple, defaultdict
from pathlib import Path
from lxml import etree as ET
import re
import click

from src.build_tei import XML
from src.build_enrich import EnrichmentTEI
from src.opt.utils import journal_error


@click.command()
@click.option("-e", "--enrich", "enrich", is_flag=True, show_default=True, default=False,
              help="Argument for automatic data enrichment")
@click.option("-v", "--validate", "validate", is_flag=True, show_default=True, default=False,
              help="Argument to execute the xml validation with the RelaxNG schema")
def run(enrich, validate):
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
        # add valid RNG

    # Enrichment of output files
    if enrich:
        # list of files
        Docs_output = namedtuple("Doc", ["name", "path"])
        files_tei = []
        for doc in list(p_output.glob('*.xml')):
            files_tei.append(Docs_output(doc.name, doc))
        # build sparql, ner, particDesc and settingDesc
        for doc in files_tei:
            xml_op = EnrichmentTEI(doc.name, doc.path)
            xml_op.annotation_NER()
            xml_op.build_profileDesc()

    # Validation
    if validate:
        # list of output files
        Docs_output = namedtuple("Doc", ["name", "path"])
        files_tei = []
        for doc in list(p_output.glob('*.xml')):
            files_tei.append(Docs_output(doc.name, doc))
        # Parsing Validation
        for doc in files_tei:
            relaxng = ET.RelaxNG(ET.parse("data/database/schema.rng"))
            parser = ET.XMLParser(recover=True)
            file = ET.parse(doc.path, parser=parser)
            if not relaxng.validate(file):
                print("Validation RNG invalid !")
                # recording error in journal
                for error in relaxng.error_log.message:
                    journal_error(rng=True, file=doc.name, message=error)

    print("Finish ! The register of possible errors has been identified at data/database/logs.txt")


if __name__ == '__main__':
    run()
