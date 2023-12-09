from pymongo import MongoClient
import os
import json


def connect_to_db(app):
    file = None
    try:
        env = os.environ.get("ENV") or "dev"  # "dev"
        file = f"mongo_db.{env}.json"

        with open(f"{os.getcwd()}/configs/{file}") as f:
            data = json.loads(f.read())
    except FileNotFoundError:
        raise FileNotFoundError(
            f"File {file} was not found in configs folder!")

    mongo_params = {
        'host': data["host"],
        'port': int(data["port"])
    }

    app.mongodb_client = MongoClient(**mongo_params)

    app.db = app.mongodb_client[data["db"]]
    app.collection_potato = app.db[data["collections"][0]]
    app.collection_tomato = app.db[data["collections"][1]]
    app.collection_pepper = app.db[data["collections"][2]]
    app.collection_is_deployed = app.db[data["collection_is_deployed"]]

    verify_deploy_data = {"is_deployed": "yes"}
    app.collection_is_deployed.insert_one(verify_deploy_data)

    global main_app
    main_app = app


def is_db_deployed(app):
    item = app.collection_is_deployed.find_one()
    if item is not None:
        return {"is_deplyed": "True"}
    else:
        return {"is_deplyed": "False"}


def save_potato(potato):
    main_app.collection_potato.insert_one(potato)


def save_tomato(tomato):
    main_app.collection_tomato.insert_one(tomato)


def save_pepper(pepper):
    main_app.collection_pepper.insert_one(pepper)
