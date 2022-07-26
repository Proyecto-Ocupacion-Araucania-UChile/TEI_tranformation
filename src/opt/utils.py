import re
import datetime

def date_process():
    x = datetime.datetime.now()
    return x.strftime("%Y-%m-%d")

def replace_pattern(input_txt: str, pattern, replace):
    r = re.findall(pattern, input_txt)
    for i in r:
        input_txt = re.sub(i, replace, input_txt)
    return input_txt

class DataTools:


    def generate_id(self):
        """
        find id if existing in JSON files, if not to create it
        :return:
        """
    def verification(self):
        """
        verication of exitence of files associated
        :return:
        """
        return
