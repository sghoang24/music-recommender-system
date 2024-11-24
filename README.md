
# Music Recommender System 🎼


## Installation ⚡️
### Requires
- **Python > 3.10**

### Setup virtual environment (`venv`)
```shell
python -m venv venv

# On Windows
cd backend
venv\Scripts\activate

# On Linux
source venv/bin/activate
pip install -r requirements.txt

# Migration database
alembic upgrade head
```

Create `.env` file following `example.env` in both `backend` and `recommendation` folder (Don't need AWS env)


## Database Migration 💾
Auto generate migration version
```shell
alembic revision --autogenerate -m <message here>
```

Upgrade migration to database
```shell
alembic upgrade head
```


## Run app with uvicorn 🚀
- **Before running remember to import data (*only need to do one time*)**
```shell
cd backend/data
python import_data.py
```

- **Run Backend Service 🛠️**
```shell
cd backend
uvicorn main:app --host 0.0.0.0 --port 8008 --reload
# Or
python main.py
```

- **Run Recommendation Service 🎹**
```shell
cd recommendation
uvicorn main:app --host 0.0.0.0 --port 8009 --reload
# Or
python main.py
```


## Run tools 🌍
- Run auto format: 
```shell
# Windows
format/format.bat
# Linux
format/format.sh
```

- Run pylint: 
```shell
pylint backend/
# OR
pylint backend/api/
# OR
pylint recommendation/
```


## Tree directory 🌗
~~~
├── backend                         - backend service.
│   ├── alembic                     - alembic version directory.
│   ├── api                         - web api related definition.
│   │   ├── database                - database configurations.
│   │   │   ├── exeute              - SQL handling, database CRUD.
│   │   │   ├── models.py           - definition of table model.
│   │   │   └── connection.py       - connection for database.
│   │   ├── errors                  - definition of error handlers.
│   │   ├── helpers                 - definition of global helpers functions.
│   │   ├── responses               - base responses for api request corresponding.
│   │   │── routes                  - web api routes.
│   │   ├── schemas                 - schemas of database models.
│   │   └── services                - logic that is not just crud related.
│   ├── core                        - application configuration, startup events, logging, constant.
│   ├── data                        - data preparation for Backend.
│   ├── fe                          - Frontend template for swagger documents.
│   ├── logger                      - export log for server process.
│   ├── tests                       - test api, code.
│   ├── utils                       - tools format, lint, test, etc.
│   ├── resources                   - image, audio, csv, etc. (ignore)
│   ├── alembic.ini                 - alembic.ini file.
│   └── main.py                     - FastAPI application creation and configuration.
│
├── recommendation                  - recommendation service.
│   ├── api                         - web api related definition.
│   │   ├── errors                  - definition of error handlers.
│   │   ├── responses               - base responses for api request corresponding.
│   │   │── routes                  - web api routes.
│   │   ├── schemas                 - schemas of database models.
│   │   └── services                - logic that is not just crud related.
│   ├── core                        - application configuration, startup events, logging, constant.
│   ├── fe                          - Frontend template for swagger documents.
│   ├── logger                      - export log for server process.
│   ├── tests                       - test api, code.
│   ├── utils                       - tools format, lint, test, etc.
│   └── main.py                     - FastAPI application creation and configuration.
│
├── logs                            - global logs folders.
├── notebooks                       - experiments notebooks.
├── requirements.txt                - package requirements file.
└── README.md                       - README instructions.
~~~
