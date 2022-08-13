import pandas as pd
import numpy as np
from SPARQLWrapper import SPARQLWrapper
from collections import namedtuple

from ..opt.utils import check_csv


# https://www.programiz.com/python-programming/datetime/strptime

class SPARQL:
    df_ent = pd.read_csv("data/database/entities.csv", encoding="utf-8")

    @staticmethod
    def __check_it__(id_):
        row = check_csv(SPARQL.df_ent, id_, 'id')
        Data = namedtuple("Data",
                          ["id_authority", "name", "date_birth", "date_death", "region", "country", "description",
                           "sex", "type", "loc", 'language'])
        if row['request'].iloc[0] is False and row['id'].str.startswith('Q') is True:
            return None
        elif row['request'].iloc[0] is True and row['id'].str.startswith('Q') is True:
            return Data(
                id_authority=row['id_authority'].iloc[0],
                name=row['name'].iloc[0],
                date_birth=row['date_birth'].iloc[0],
                date_death=row['date_end'].iloc[0],
                region=row['region'].iloc[0],
                country=row['country'].iloc[0],
                description=row['description'].iloc[0],
                sex=row['sex'].iloc[0],
                type=row['type'].iloc[0],
                loc="loc",
                language='language'
            )
        else:
            return Data(
                id_authority=row['id_authority'].iloc[0],
                name=row['name'].iloc[0],
                date_birth=row['date_birth'].iloc[0],
                date_death=row['date_end'].iloc[0],
                region=row['region'].iloc[0],
                country=row['country'].iloc[0],
                description=row['description'].iloc[0],
                sex=row['sex'].iloc[0],
                type=row['type'].iloc[0],
                loc="loc",
                language='es'
            )


    @staticmethod
    def run_sparql(id_):
        row = SPARQL.__check_it__(id_)
        if row is None:
            print("faire requete")
            # SPARQL.df_ent.to_csv("data/database/entities.csv", encoding="utf-8")
            Data = namedtuple("Data",
                              ["id_authority", "name", "date_birth", "date_death", "region", "country", "description",
                               "sex"])
            return Data(
                id_authority=np.nan,
                name=np.nan,
                date_birth=np.nan,
                date_death=np.nan,
                region=np.nan,
                country=np.nan,
                description=np.nan,
                sex="0",
            )
        else:
            return row
