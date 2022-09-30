# TEI transformation

## Summary

CLI to convert OCR data in XML-ALTO format to TEI p5 encoding from a specific [SegmOnto](https://segmonto.github.io/) ontology. 

It takes over and modifies the [ALTO2TEI](https://github.com/kat-kel/alto2tei) project developed by Kelly Christensen in the Gallic(orpor)a project.

The works as follows: Order and group the files within input/ -> parse the ALTO files -> build the **\<teiHeader>** (with `database/`) -> build the **\<sourceDesc>** -> build the **\<text>** according to the ontology

## Enrichment 

With the `-e` option enabled, the XML-TEI files are then parsed with to detect the following entities with the NER model:
- **\<persName>**
- **\<orgName>**
- **\<date>**
- **\<placeName>**

An [Entity-Fishing](https://github.com/Lucaterre/spacyfishing) system has been implemented in order to be able to query (sparql) places and people on Wikidata databases in `src/enrichment/`.

## Tree
```
Project
|
├── data
│   ├── database
 |    |   ├── database
 |    |    |          ├── ODD_Letters.html
 |    |    |          └── ODD_Letters.xml
│   │   ├── araucania_inventory.csv
│   │   ├── entities.csv
│   │   ├── logs.txt
│   │   ├──resp.json
│   │   └── schema_letter.rng
|
│   ├── models
│   │   └── araucania_NER_model
|   |
│   ├── input
│   └── output
|
├── requirements.txt
├── run.py
|
└── src
    ├── __init__.py
    ├── build_body.py
    ├── build_enrich.py
    ├── build_tei.py
    |
    ├── enrichment
    │   ├── __init__.py
    │   ├── nlp.py
    │   ├── query.py
    │   └── sparql.py
    |
    ├── opt
    │   ├── __init__.py
    │   ├── extract_alto.py
    │   ├── inventory.py
    │   ├── surface_and_desc.py
    │   └── utils.py
    |
    ├── sourceDoc_attributes.py
    ├── sourceDoc.py
    ├── teiheader.py
    └── text_data.py
```
