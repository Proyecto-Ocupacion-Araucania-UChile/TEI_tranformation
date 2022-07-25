from lxml import etree


class XML:
    NS = {'alto': "http://www.loc.gov/standards/alto/ns-v4#"}
    tags = None
    root = None
    date = None

    def __init__(self, name, path):
        self.name = name
        self.path = path

    def __load__(self):
        return

    def preparation_metadada(self):
        from .opt.build_alto import ALTO

        self.tags = ALTO.labels(self)
        self.root = etree.Element("TEI", {"xmlns": "http://www.tei-c.org/ns/1.0"})



