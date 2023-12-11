from fastapi import FastAPI
from kafka.kafka_consumer import *
from mongo.mongodb import connect_to_db
from image_api.plant_api import router as image_plant_router

import uvicorn
import os
import json
import threading


app = FastAPI()


def get_url():
    file = None
    try:
        env = os.environ.get("ENV") or "dev"
        file = f"config.{env}.json"

        print(f"Used the following FastAPI config: {file}")

        with open(f"{os.getcwd()}/configs/{file}") as f:
            data = json.loads(f.read())
    except FileNotFoundError:
        raise FileNotFoundError(
            f"File {file} was not found in configs folder!")

    url = data['service_url']
    port = data['service_port']

    return url, port


@app.get("/ping")
async def root():
    return {"Hello, I am alive"}


def connect_to_db_thread():
    connect_to_db(app)


def consume_messages_thread():
    consume_messages()


def on_start():
    # Start connect_to_db in a separate thread
    db_thread = threading.Thread(target=connect_to_db_thread)
    db_thread.start()

    # Start consume_messages in a separate thread
    consume_thread = threading.Thread(target=consume_messages_thread)
    consume_thread.start()


@app.on_event("startup")
def startup():
    on_start()


@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()


app.include_router(image_plant_router)


if __name__ == "__main__":
    hostnamevalue, portvalue = get_url()
    uvicorn.run(app, host=hostnamevalue, port=portvalue)
