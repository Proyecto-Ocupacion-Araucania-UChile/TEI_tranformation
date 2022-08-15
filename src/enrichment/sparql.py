import pandas as pd
import numpy as np
from SPARQLWrapper import SPARQLWrapper, SPARQLExceptions, JSON
from collections import namedtuple

from ..opt.utils import check_csv, journal_error
from .query import QUERY_GEO, QUERY_PERS


class SPARQL:
    """
    Class to run sparql request
    """
    df_ent = pd.read_csv("data/database/entities.csv", encoding="utf-8")

    @staticmethod
    def __check_it__(id_):
        """
        Pre function to verify if id
        :param id_: id of entity
        :return: namedtuple or None
        """
        # Get row
        row = check_csv(SPARQL.df_ent, id_, 'id')
        Data = namedtuple("Data",
                          ["id_authority", "name", "date_birth", "date_death", "region", "country", "description",
                           "sex", "type", "loc", 'language'])
        # If it finds token id but sparql request wasn't executed
        if row['request'].iloc[0] == False and row['id'].str.startswith('Q').iloc[0] == True:
            return None
        # find token id and the sparql request was executed
        elif row['request'].iloc[0] == True and row['id'].str.startswith('Q').iloc[0] == True:
            return Data(
                id_authority=row['id_authority'].iloc[0] if not pd.isna(row['id_authority'].iloc[0]) else None,
                name=row['name'].iloc[0] if not pd.isna(row['name'].iloc[0]) else None,
                date_birth=row['date_birth'].iloc[0] if not pd.isna(row['date_birth'].iloc[0]) else None,
                date_death=row['date_end'].iloc[0] if not pd.isna(row['date_end'].iloc[0]) else None,
                region=row['region'].iloc[0] if not pd.isna(row['region'].iloc[0]) else None,
                country=row['country'].iloc[0] if not pd.isna(row['country'].iloc[0]) else None,
                description=row['description'].iloc[0] if not pd.isna(row['description'].iloc[0]) else None,
                sex=row['sex'].iloc[0] if not pd.isna(row['sex'].iloc[0]) else None,
                type=row['type'].iloc[0] if not pd.isna(row['type'].iloc[0]) else None,
                loc=row['geo_loc'].iloc[0] if not pd.isna(row['geo_loc'].iloc[0]) else None,
                language='en'
            )
        # if the id cannot be executed as a sparql request
        else:
            return Data(
                id_authority=row['id_authority'].iloc[0] if not pd.isna(row['id_authority'].iloc[0]) else None,
                name=row['name'].iloc[0] if not pd.isna(row['name'].iloc[0]) else None,
                date_birth=row['date_birth'].iloc[0] if not pd.isna(row['date_birth'].iloc[0]) else None,
                date_death=row['date_end'].iloc[0] if not pd.isna(row['date_end'].iloc[0]) else None,
                region=row['region'].iloc[0] if not pd.isna(row['region'].iloc[0]) else None,
                country=row['country'].iloc[0] if not pd.isna(row['country'].iloc[0]) else None,
                description=row['description'].iloc[0] if not pd.isna(row['description'].iloc[0]) else None,
                sex=row['sex'].iloc[0] if not pd.isna(row['sex'].iloc[0]) else None,
                type=row['type'].iloc[0] if not pd.isna(row['type'].iloc[0]) else None,
                loc=row['geo_loc'].iloc[0] if not pd.isna(row['geo_loc'].iloc[0]) else None,
                language='es'
            )

    @staticmethod
    def execute_query(id_, type_: str):
        """
        Function to request query in database of wikidata according to the type of entity.
        :param id_: TOKEN
        :param type_: type of entity 'PERS' or 'LOC'
        :return: None
        """
        # initiate database to request
        sparql = SPARQLWrapper("https://query.wikidata.org/sparql")
        # dataframe
        df = SPARQL.df_ent
        try:
            # set query according to type
            if type_ == 'PERS':
                sparql.setQuery(QUERY_PERS.replace('TOKEN', str(id_)))
            elif type_ == 'LOC':
                sparql.setQuery(QUERY_GEO.replace('TOKEN', str(id_)))
            # return format and result
            sparql.setReturnFormat(JSON)
            ret = sparql.queryAndConvert()
            results = ret['results']['bindings'][0]
            # save data
            if type_ == 'PERS':
                # Get values
                if 'sex' in results:
                    if results['sex']['value'] == 'male':
                        sex = str(1)
                    elif results['sex']['value'] == 'female':
                        sex = str(2)
                    else:
                        sex = str(0)
                else:
                    sex = np.nan
                if 'VIAF' in results:
                    id_authority = str(results['VIAF']['value'])
                else:
                    id_authority = np.nan
                if 'description' in results:
                    description = results['description']['value']
                else:
                    description = np.nan
                if 'date_birth' in results:
                    date_birth = results['date_birth']['value'][:-10]
                else:
                    date_birth = np.nan
                if 'date_death' in results:
                    date_end = results['date_death']['value'][:-10]
                else:
                    date_end = np.nan
                if 'country' in results:
                    country = results['country']['value']
                else:
                    country = np.nan
                # Update csv
                df.loc[df['id'] == id_, ['country', 'description', 'id_authority', 'sex', 'date_birth', 'date_end',
                                         'request']] = [country, description, id_authority, sex, date_birth, date_end,
                                                        True]
                # Clean
                del sex, description, date_birth, id_authority, date_end, country, ret, results

            elif type_ == 'LOC':
                # Get values
                if 'loc' in results:
                    geo_loc = str(results['loc']['value'][6:-1])
                else:
                    geo_loc = np.nan
                if 'description' in results:
                    description = results['description']['value']
                else:
                    description = np.nan
                if 'region' in results:
                    region = results['region']['value']
                else:
                    region = np.nan
                if 'GeoNames' in results:
                    id_authority = results['GeoNames']['value']
                else:
                    id_authority = np.nan
                if 'instance' in results:
                    type_csv = results['instance']['value']
                else:
                    type_csv = np.nan
                if 'country' in results:
                    country = results['country']['value']
                else:
                    country = np.nan

                # Update csv
                df.loc[df['id'] == id_, ['type', 'region', 'country', 'description', 'id_authority', 'geo_loc',
                                         'request']] = [type_csv, region, country, description, id_authority, geo_loc,
                                                        True]
                # Clean
                del geo_loc, description, region, id_authority, type_csv, country, ret, results
        # Registering errors requests
        except (SPARQLExceptions.EndPointInternalError, KeyError) as errors:
            journal_error(file='entities.csv', error=errors, name=str(id_))
            df.loc[df['id'] == id_, ['request']] = [True]
        # Update dataframe
        df.to_csv("data/database/entities.csv", encoding="utf-8", index=False)

    @staticmethod
    def run_sparql(id_, type_: str) -> namedtuple:
        """
        run to verify if data exist or execute query request
        :param id_:
        :param type_:
        :return:
        """
        # verify id status
        data = SPARQL.__check_it__(id_)
        # run sparql request and reexecute function
        if data is None:
            SPARQL.execute_query(id_, type_)
            return SPARQL.run_sparql(id_, type_)
        # return directly tuples data of row
        else:
            return data
