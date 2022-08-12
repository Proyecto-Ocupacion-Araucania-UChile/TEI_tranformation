import re
import datetime
import json
import numpy as np
from lxml import etree as ET
import pandas as pd
import os


def date_process() -> str:
    """
    function to import date of execution in str
    :return: str date
    """
    x = datetime.datetime.now()
    return x.strftime("%Y-%m-%d")


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


def read_json(file: str, encoding="utf-8") -> list or dict:
    """
    Function to read json file
    :param file: path of json file
    :param encoding: choice of encoding. By default it's utf-8
    :return: json
    """
    with open(file, encoding=encoding, mode="r") as f:
        f_json = json.load(f)
    return f_json


def write_xml(**kwargs):
    """

    :param kwargs:
    :return: None
    """
    if 'path' in kwargs:
        with open(kwargs['path'], 'wb') as f:
            ET.ElementTree(kwargs['root']).write(f, encoding="utf-8", xml_declaration=True, pretty_print=True)
    else:
        with open(f"./data/output/{kwargs['type']}_AH0{kwargs['id']}.xml", 'wb') as f:
            ET.ElementTree(kwargs['root']).write(f, encoding="utf-8", xml_declaration=True, pretty_print=True)


def check_csv(df: pd.DataFrame, element, column: str) -> pd.DataFrame:
    """
    function to check if elements exist in csv
    :param df: dataframe
    :param element: name which you want to identify
    :param column: columns names where you want identify your element
    :return: dataframe row
    """
    return df.loc[df[column] == element]


def generate_id(ent_: str) -> str:
    """
    Generate an id with its name entities
    :return: str id
    """
    return ent_ + "_" + str(np.random.random_integers(10000, high=99999))


def journal_error(**kwargs):
    if os.path.isfile("data/database/logs.txt"):
        with open("data/database/logs.txt", "a") as f:
            f.write(
                f"""{kwargs["file"]}: entitie "{kwargs['name']}", error {kwargs['error']}""")
            f.write("\n")
    else:
        with open("data/database/logs.txt", "w") as f:
            f.write(
                f"""{kwargs["file"]}: entitie "{kwargs['name']}", error {kwargs['error']}""")
            f.write("\n")
