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
    app.db_name_plant = app.mongodb_client[data["db_name_plant"]]
    app.col_name_plant_potato = app.db_name_plant[data["col_name_plant"][0]]
    app.col_name_plant_tomato = app.db_name_plant[data["col_name_plant"][1]]
    app.col_name_plant_pepper = app.db_name_plant[data["col_name_plant"][2]]
    app.col_name_plant_is_deployed = app.db_name_plant[data["col_is_deployed"]]

    verify_deploy_data = {"is_deployed": "yes"}
    app.collection_is_deployed.insert_one(verify_deploy_data)

    global main_app
    main_app = app


def is_db_deployed(app):
    item = app.col_name_plant_is_deployed.find_one()
    if item is not None:
        return {"is_deplyed": "True"}
    else:
        return {"is_deplyed": "False"}


def save_potato(potato):
    main_app.col_name_plant_potato.insert_one(potato)


def save_tomato(tomato):
    main_app.col_name_plant_tomato.insert_one(tomato)


def save_pepper(pepper):
    main_app.col_name_plant_pepper.insert_one(pepper)
