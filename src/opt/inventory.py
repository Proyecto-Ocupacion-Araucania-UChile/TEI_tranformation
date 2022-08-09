import pandas as pd
from pandas import DataFrame
from pandas.core.series import Series
import numpy as np
from numpy import ndarray
from collections import namedtuple

from .utils import replace_pattern, check_csv


class Inventory:
    csv = "data/database/araucania_inventory.csv"
    df = pd.read_csv(csv, encoding="utf-8")

    def __init__(self, id_):
        self.id = int(id_)
        self.row = check_csv(self.df, self.id, 'Id')

    def _author(self) -> list:
        row = self.row
        list_author = []
        if row['Author'].iloc[0] is not np.nan:
            list_author.append(row.Author.iloc[0])
        else:
            list_author.append("Unknow")
        if row['Author2'].iloc[0] is not np.nan:
            list_author.append(row.Author2.iloc[0])
        return list_author

    @staticmethod
    def _date(date: Series) -> ndarray:
        return np.vectorize(replace_pattern)(date, "/", "-")

    def metadata(self) -> namedtuple:
        row = self.row
        Metadata = namedtuple('Metadata', ['box', 'type_file', 'title', 'author', 'date', 'loc', 'nb_page'])
        box = row.Box.iloc[0]
        author = self._author()
        type_file = row.Type.iloc[0]
        title = row.Title.iloc[0]
        date = self._date(row['Date']).item(0)
        nb_page = len(row['files'].iloc[0].split(";")) - 1
        if row.Location.array[0] != np.nan:
            loc = row['Location'].apply(lambda x: str(x).split(';'))
        else:
            loc = "Unknow"
        return Metadata(box, type_file, title, author, date, loc, nb_page)
