import os

from utils import Tools

class XmlALTO:
    NS = {'alto': "http://www.loc.gov/standards/alto/ns-v4#"}

    def __init__(self, path, _current_path):
        self.path = os.path.join(_current_path, path)

    def load(self):
        return

    def metadada(self):
        return



