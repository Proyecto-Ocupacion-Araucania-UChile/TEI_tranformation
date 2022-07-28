import re
import datetime
import json
import numpy as np
from lxml import etree as ET


class Tools:
    @staticmethod
    def date_process():
        """
        function to import date of execution in str
        :return: str date
        """
        x = datetime.datetime.now()
        return x.strftime("%Y-%m-%d")

    @staticmethod
    def replace_pattern(input_txt: str, pattern: str, replace: str) -> str:
        """
        Function to replace an element by an other element in a text
        :param input_txt: text which need to correct it
        :param pattern: element who want to replace
        :param replace: element will replace it
        :return: text corrected
        """
        r = re.findall(pattern, input_txt)
        for i in r:
            input_txt = re.sub(i, replace, input_txt)
        return input_txt

    @staticmethod
    def read_json(file: str, encoding="utf-8"):
        """
        Function to read json file
        :param file: path of json file
        :param encoding: choice of encoding. By default it's utf-8
        :return: json
        """
        with open(file, encoding=encoding, mode="r") as f:
            f_json = json.load(f)
        return f_json

    @staticmethod
    def write_xml(file, root):
        with open(f'./data/output/{file}.xml', 'wb') as f:
            ET.ElementTree(root).write(f, encoding="utf-8", xml_declaration=True, pretty_print=True)


###build a fumction to find if id exist. if exist find id in csv and put in ref
### if not exist, create id, push in csv and put in xml:id

class DataTools:

    @staticmethod
    def generate_id(ent_: str) -> str:
        """
        Generate an id with its name entities
        :return: str id
        """
        return ent_ + "_" + str(np.random.random_integers(10000, high=99999))

    def verification(self):
        """
        verication of exitence of files associated
        :return:
        """
        return
