```bash
.
├── app
│   ├── configs
│   │   ├── config.py
│   │   └── __init__.py
│   ├── __init__.py
│   ├── main.py
│   ├── models
│   │   ├── drugs.py
│   │   ├── __init__.py
│   │   ├── pubmed_trials.py
│   │   └── referenced_drugs.py
│   └── utils
│       ├── __init__.py
│       └── utils.py
├── data
│   ├── landing
│   │   ├── clinical_trials.csv
│   │   ├── pubmed.csv
│   │   └── pubmed.json
│   └── staging
│       └── curated_2024-11-03 13:12:55.587911
├── referential_drugs
│   └── drugs.csv
├── requirements-dev.txt
└── tests
    ├── integration
    │   └── test_e2e.py
    ├── test_main.py
    ├── test_models.py
    └── test_utils.py
