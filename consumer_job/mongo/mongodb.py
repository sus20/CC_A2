from pymongo import MongoClient
import os
import json


def connect_to_db(app):
    print("fetching the file from environment.")
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

    print("consumer connecting to db.....")
    app.mongodb_client = MongoClient(**mongo_params)
    app.db_name_plant = app.mongodb_client[data["db_name_plant"]]
    app.col_name_plant_potato = app.db_name_plant[data["col_name_plant"][0]]
    app.col_name_plant_tomato = app.db_name_plant[data["col_name_plant"][1]]
    app.col_name_plant_pepper = app.db_name_plant[data["col_name_plant"][2]]
    app.col_name_plant_is_deployed = app.db_name_plant[data["col_is_deployed"]]
    print("consumer connected to db")

    global main_app
    main_app = app


def save_potato(potato):
    main_app.col_name_plant_potato.insert_one(potato)


def save_tomato(tomato):
    main_app.col_name_plant_tomato.insert_one(tomato)


def save_pepper(pepper):
    main_app.col_name_plant_pepper.insert_one(pepper)
