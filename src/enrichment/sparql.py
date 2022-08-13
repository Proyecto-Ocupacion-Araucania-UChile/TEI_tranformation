import pandas as pd
import numpy as np
from SPARQLWrapper import SPARQLWrapper, SPARQLExceptions, JSON
from collections import namedtuple

from ..opt.utils import check_csv, journal_error
from .query import QUERY_GEO, QUERY_PERS


# https://www.programiz.com/python-programming/datetime/strptime

class SPARQL:
    df_ent = pd.read_csv("data/database/entities.csv", encoding="utf-8")

    @staticmethod
    def __check_it__(id_):
        """
        Pre function to verify if id
        :param id_:
        :return:
        """
        #Get row
        row = check_csv(SPARQL.df_ent, id_, 'id')
        Data = namedtuple("Data",
                          ["id_authority", "name", "date_birth", "date_death", "region", "country", "description",
                           "sex", "type", "loc", 'language'])
        # If find token id but sparql request wasn't executed
        if row['request'].iloc[0] is False and row['id'].str.startswith('Q') is True:
            return None
        # find token id and the sparql request was executed
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
                language='en'
            )
        # if the id cannot be executed as a sparql request
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
    def execute_query(id_, type_: str):
        sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
        df = SPARQL.df_ent
        try:
            if type_ == 'PERS':
                sparql.setQuery(QUERY_PERS.replace('TOKEN', str(id_)))
            elif type_ == 'LOC':
                sparql.setQuery(QUERY_GEO.replace('TOKEN', str(id_)))
            sparql.setReturnFormat(JSON)
            ret = sparql.queryAndConvert()
            results = ret['results']['bindings'][0]
            if type_ == 'PERS':
                print(results)
            elif type_ == 'LOC':
                geo_loc = str(results['loc']['value'][6:-1])
                #df.loc[df['id'] == id_, ['type', 'region', 'country', 'description', 'id_authority', 'geo_loc']] = ['blabla','je suis changé']
        # Registering errors requests
        except SPARQLExceptions as error:
            journal_error(file='entities.csv', error=error, name=str(id_))
        #Update dataframe
        #SPARQL.df_ent = df

    @staticmethod
    def run_sparql(id_, type_):
        # verify id status
        row = SPARQL.__check_it__(id_)
        # run sparql request
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
        # return directly tuples data of row
        else:
            return row
