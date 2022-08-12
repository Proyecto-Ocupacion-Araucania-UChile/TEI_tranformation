import pandas as pd
from collections import namedtuple

from ..opt.utils import check_csv

#https://www.programiz.com/python-programming/datetime/strptime

class SPARQL:
    df_ent = pd.read_csv("data/database/entities.csv", encoding="utf-8")

    @staticmethod
    def __check_it__(id_):
        row = check_csv(SPARQL.df_ent, id_, 'id')
        Data = namedtuple("Data", ["name", "path"])
        if row['request'].iloc[0] != "TRUE":
            print("faire sparql")
        else:
