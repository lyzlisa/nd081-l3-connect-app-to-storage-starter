import os
import json
from pathlib import Path

basedir = os.path.abspath(os.path.dirname(__file__))


def get_from_tf_state(name):
    with open(Path(basedir)/"infra/state.json") as file:
        state = json.load(file)
        return state["outputs"][name]["value"]


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret-key'

    SQL_SERVER = os.environ.get('SQL_SERVER') or get_from_tf_state('sql_server')
    SQL_DATABASE = os.environ.get('SQL_DATABASE') or get_from_tf_state('sql_database')
    SQL_USER_NAME = os.environ.get('SQL_USER_NAME') or get_from_tf_state('sql_user_name')
    SQL_PASSWORD = os.environ.get('SQL_PASSWORD') or get_from_tf_state('sql_password')
    SQLALCHEMY_DATABASE_URI = (
        f"mssql+pyodbc://{SQL_USER_NAME}:{SQL_PASSWORD}@{SQL_SERVER}:1433/{SQL_DATABASE}?driver=ODBC+Driver+17+for+SQL+Server"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    BLOB_ACCOUNT = os.environ.get('BLOB_ACCOUNT') or get_from_tf_state('blob_account')
    BLOB_STORAGE_KEY = os.environ.get('BLOB_STORAGE_KEY') or get_from_tf_state('blob_storage_key')
    BLOB_CONTAINER = os.environ.get('BLOB_CONTAINER') or get_from_tf_state('blob_container')
