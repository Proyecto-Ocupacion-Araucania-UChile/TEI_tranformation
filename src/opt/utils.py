import re
import datetime
import json
import numpy as np


class Tools:
    @staticmethod
    def date_process():
        x = datetime.datetime.now()
        return x.strftime("%Y-%m-%d")

    @staticmethod
    def replace_pattern(input_txt: str, pattern: str, replace: str) -> str:
        r = re.findall(pattern, input_txt)
        for i in r:
            input_txt = re.sub(i, replace, input_txt)
        return input_txt

    @staticmethod
    def read_json(file: str, encoding="utf-8"):
        with open(file, encoding=encoding, mode="r") as f:
            f_json = json.load(f)
        return f_json


###build a fumction to find if id exist. if exist find id in csv and put in ref
### if not exist, create id, push in csv and put in xml:id

class DataTools:

    @staticmethod
    def generate_id(ent_: str) -> str:
        """
        find id if existing in JSON files, if not to create it
        :return:
        """

        return ent_ + "_" + str(np.random.random_integers(10000, high=99999))

    def verification(self):
        """
        verication of exitence of files associated
        :return:
        """
        return
