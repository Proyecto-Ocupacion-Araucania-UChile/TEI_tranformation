# TEI_tranformation

Project
|
├── data
│   ├── database
│   │   ├── araucania_inventory.csv
│   │   ├── entities.csv
│   │   ├── logs.txt
│   │   └── resp.json
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
