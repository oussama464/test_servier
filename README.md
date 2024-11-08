## running pre-commit

```bash
pip install pre-commit
pre-commit install

pre-commit run --all-files -v
```
## Running tests
```bash
pytest -vv -s tests/
or
PYTHONPATH=. pytest -vv -s tests/
```
## packaging the code

```bash
pip install build

python -m build --sdist --wheel .
```

## project tree

```bash
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
│       ├── curated_2024-11-07 23:15:23.353023.json
│       └── curated_2024-11-07 23:45:59.475987.json
├── Makefile
├── pyproject.toml
├── README.md
├── referential_drugs
│   └── drugs.csv
├── requirements-dev.txt
├── run.sh
├── tests
│   ├── conftest.py
│   ├── integration
│   │   └── test_e2e.py
│   ├── test_main.py
│   ├── test_models.py
│   └── test_utils.py
└── version.txt
