###build a fumction to find if id exist. if exist find id in csv and put in ref
### if not exist, create id, push in csv and put in xml:id


#https://www.programiz.com/python-programming/datetime/strptime
def verification(self):
    """
    verication of exitence of files associated
    :return:
    """
    return


QUERY_PERS = """
PREFIX wd: <http://www.wikidata.org/entity/> 
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX schema: <http://schema.org/> 
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX dc:     <http://purl.org/dc/elements/1.1/>
PREFIX xsd:    <http://www.w3.org/2001/XMLSchema#>


SELECT ?country ?date_birth ?date_death ?name ?id ?description ?sex
WHERE {
          BIND (wd:Q4233309 AS ?id) #get entitie
  
  OPTIONAL {
  ?id rdfs:label ?name . #get label of entitie in english
  FILTER (langMatches(lang(?name), "EN"))
   }
  
  OPTIONAL {
    ?id schema:description ?description . #get label of entitie in english
  FILTER (langMatches(lang(?description), "EN"))
  }
  
  
  OPTIONAL {
    ?id wdt:P625 ?loc . #get latitude and longitude in coordinate location
  }
  OPTIONAL {
            ?id wdt:P21 ?sex_id . #get label of sex in english
            ?sex_id rdfs:label ?sex .
            FILTER (langMatches(lang(?sex), "EN"))
          }
  OPTIONAL {
            ?id wdt:P27 ?country_id . #get label of country in english
            ?country_id rdfs:label ?country .
            FILTER (langMatches(lang(?country), "EN"))
          }
  OPTIONAL {
            ?id wdt:P569 ?date_birth . #get date of birth in english
          }
  OPTIONAL {
            ?id wdt:P570 ?date_death .
  }
  OPTIONAL {
            ?id wdt:P1566 ?GeoNames . #get id geoname
          }
  SERVICE wikibase:label { bd:serviceParam wikibase:language 'en' }
}
LIMIT 1
"""


QUERY_GEO = """
PREFIX wd: <http://www.wikidata.org/entity/> 
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX schema: <http://schema.org/> 
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>

SELECT ?country ?region ?GeoNames ?name ?id ?instance ?loc ?description
WHERE {
          BIND (wd:Q2887 AS ?id) #get entitie
  
  OPTIONAL {
  ?id rdfs:label ?name . #get label of entitie in english
  FILTER (langMatches(lang(?name), "EN"))
   }
  
  OPTIONAL {
    ?id schema:description ?description . #get label of entitie in english
  FILTER (langMatches(lang(?description), "EN"))
  }
  
  
  OPTIONAL {
    ?id wdt:P625 ?loc . #get latitude and longitude in coordinate location
  }
  OPTIONAL {
            ?id wdt:P31 ?instance_id . #get label of instance in english
            ?instance_id rdfs:label ?instance .
            FILTER (langMatches(lang(?instance), "EN"))
          }
  OPTIONAL {
            ?id wdt:P17 ?country_id . #get label of country in english
            ?country_id rdfs:label ?country .
            FILTER (langMatches(lang(?country), "EN"))
          }
  OPTIONAL {
            ?id wdt:P131 ?region_id . #get label of region in english
            ?region_id rdfs:label ?region .
            FILTER (langMatches(lang(?region), "EN"))
          }
  OPTIONAL {
            ?id wdt:P1566 ?GeoNames . #get id geoname
          }
}
LIMIT 1
"""
