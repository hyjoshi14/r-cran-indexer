## R CRAN Indexer

This repository utilises [Flask Restplus](https://flask-restplus.readthedocs.io/en/stable/) and [SQLite](https://www.sqlite.org/index.html) to provide an API endpoint to search for R Packages registered on CRAN.

### Sections
- [Prerequisites](#Prerequisites)
- [Installation](#Installation)
- [Setting up R CRAN Indexer](#Setting-up-R-CRAN-Indexer)
- [Querying R CRAN Indexer](#Querying-R-CRAN-Indexer)


### Prerequisites
- [Python 3.7](https://www.python.org/downloads/release/python-376/)
- [SQLite](https://www.sqlite.org/download.html)


### Installation
1. Clone/Download the repo into your machine
2. Switch to the directory where the repo is located and set up a virtual environment
```
cd ~/path-to-r-cran-indexer/
virtualenv .
```
3. Activate the virtualenv
```
source bin/activate
```
4. Install the packages in the `requirements.txt` file
```
pip install -r requirements.txt
```

### Setting up R CRAN Indexer
Once the packages are installed R CRAN Indexer run the following commands to backfill data and start the application.

In a separate shell/as a background process backfill data
```
python backfill_package_info.py --processes 10 --packages 10
```
To understand more about the script run
```
python backfill_package_info --help
```

In a separate shell/as a background process start the application on `localhost:8080`
```
python run.py
```

### Querying R CRAN Indexer
1. Navigate to `localhost:8080` or to where the application is running
2. Use the Swagger Document that appears to understand the `/search` endpoint and query it as well
