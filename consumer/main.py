from fastapi import FastAPI, HTTPException
from kafka.kafka_consumer import consume_messages, shutdown
from fastapi.middleware.cors import CORSMiddleware
from mongo.mongodb import connect_to_db, is_db_deployed

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


@app.get("/shutdown")
def stop_consuming():
    try:
        shutdown()
        uvicorn.stop()
        return {"status": "stopped"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.on_event("startup")
def startup_db_client():
    connect_to_db(app)
    consume_messages()


@app.on_event("shutdown")
def shutdown_db_client():
    app.mongodb_client.close()


@app.get("/is_deployed")
def is_deployed():
    return is_db_deployed(app)


if __name__ == "__main__":

    hostnamevalue, portvalue = get_url()

    uvicorn.run(app, host=hostnamevalue, port=portvalue)
