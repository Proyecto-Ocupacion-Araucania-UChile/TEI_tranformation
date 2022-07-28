import pandas as pd
from pandas import DataFrame
from pandas.core.series import Series
import numpy as np
from numpy import ndarray
from collections import namedtuple

from .utils import Tools


class Inventory:
    csv = "data/database/araucania_inventory.csv"
    df = pd.read_csv(csv, encoding="utf-8")

    def __init__(self, filename):
        self.filename = filename
        self.id = self.__find_id__()
        self.row = self._row_select()

    def __find_id__(self) -> int:
        return int(self.filename[:3])

    def _row_select(self) -> DataFrame:
        df = self.df
        return df.loc[df['Id'] == self.id]

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
        return np.vectorize(Tools.replace_pattern)(date, "/", "-")

    def metadata(self) -> namedtuple:
        row = self.row
        Metadata = namedtuple('Metadata', ['box', 'type_file', 'title', 'author', 'date', 'loc', 'nb_page'])
        box = row.Box.iloc[0]
        author = self._author()
        type_file = row.Type.iloc[0]
        title = row.Title.iloc[0]
        date = self._date(row['Date']).item(0)
        nb_page = row['files'].str.split(";").str.len() - 1
        if row.Location.array[0] != np.nan:
            loc = row['Location'].apply(lambda x: str(x).split(';'))
        else:
            loc = "Unknow"
        return Metadata(box, type_file, title, author, date, loc, nb_page)
