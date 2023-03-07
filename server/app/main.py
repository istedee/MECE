import json
import uvicorn
import os
import redis
from dotenv import load_dotenv

from fastapi import FastAPI
from kafka import KafkaProducer

import models
from db import engine, SessionLocal

load_dotenv(verbose=True)

app = FastAPI()

# Init db if not existing
# Database connection function for use in routers
# And accross the REST API
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def serializer(messages):
    return json.dumps(messages).encode('utf-8')

if os.environ.get("BOOTSTRAP-SERVERS"):
    print("Found bootstrap server env variable")
    # producer = KafkaProducer(
    # bootstrap_servers=os.environ.get("BOOTSTRAP-SERVERS"),
    # value_serializer=serializer
    # )
else:
    print("Environment variable for Kafka not found")
    print("Use localhost as default")
    # producer = KafkaProducer(
    # bootstrap_servers=["localhost:9092"],
    # value_serializer=serializer
    # )

# Redis config:
redis_client = redis.Redis(host=os.environ.get("REDIS_HOST"), port=os.environ.get("REDIS_PORT"))

models.Base.metadata.create_all(bind=engine)

from routes import messages, users, healthcheck, chatrooms

app.include_router(messages.router)
app.include_router(users.router)
app.include_router(healthcheck.router)
app.include_router(chatrooms.router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
