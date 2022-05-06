Chem dataset
==============================

Parsing and filtering 2d molecules' data

Project Organization
------------

    ├── LICENSE
    ├── Makefile            <- Makefile with commands like `make data` or `make train`
    ├── README.md           <- The top-level README for developers using this project.
    ├── data
    │   ├── concat          <- Data to concatenate
    │   ├── interim         <- Intermediate data that has been transformed.
    │   ├── processed       <- The final, canonical data sets for modeling.
    │   └── raw             <- The original, immutable data dump.
    │   
    ├── docs                <- A default Sphinx project; see sphinx-doc.org for details
    │   
    │   
    ├── notebooks           <- Jupyter notebooks. Naming convention is a number (for ordering),
    │                          the creator's initials, and a short `-` delimited description, e.g.
    │                          `1.0-jqp-initial-data-exploration`.
    │   
    ├── references          <- Data dictionaries, manuals, and all other explanatory materials.
    │
    ├── reports             <- Generated analysis as HTML, PDF, LaTeX, etc.
    │   └── figures         <- Generated graphics and figures to be used in reporting
    │
    ├── requirements.txt    <- The requirements file for reproducing the analysis environment, e.g.
    │                         generated with `pip freeze > requirements.txt`
    │
    ├── setup.py            <- makes project pip installable (pip install -e .) so chem_dataset can be imported
    ├── chem_dataset                    <- Source code for use in this project.
    │   ├── __init__.py                 <- Makes chem_dataset a Python module
    │   │
    │   ├── data                        <- Scripts to download or generate data
    │   │   ├── dup.py                  <- Remove duplicates 
    │   │   ├── ftp_download.py         <- Download data files from ftp
    │   │   ├── parser_multi_pool.py    <- Parsing data by multiprocess lib
    │   │   └── parser_ray_pubchem.py   <- Parsing data by ray
    │   │
    │   ├── features        <- Scripts to turn raw data into features for modeling
    │   │   └── build_features.py
    │   │
    │   └── visualization   <- Scripts to create exploratory and results oriented visualizations
    │       └── visualize.py
    │
    └── tox.ini             <- tox file with settings for running tox; see tox.readthedocs.io


--------

<p><small>Project based on the <a target="_blank" href="https://drivendata.github.io/cookiecutter-data-science/">cookiecutter data science project template</a>. #cookiecutterdatascience</small></p>
