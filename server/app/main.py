import uvicorn
import time
import os
from dotenv import load_dotenv

from fastapi import FastAPI

import models
from db import engine, SessionLocal

from kafka import KafkaAdminClient
from kafka.admin import NewTopic
from kafka.errors import TopicAlreadyExistsError

load_dotenv(verbose=True)

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    #wait for Kafka broker to be ready
    time.sleep(1)
    # Kafka Admin Client
    client = KafkaAdminClient(
        bootstrap_servers=os.environ.get("BOOTSTRAP-SERVERS"))
    # Creating topic
    topic = NewTopic(name=os.environ.get("TOPIC_MESSAGES_BASIC_NAME"),
                     num_partitions=int(os.environ.get("TOPIC_MESSAGES_BASIC_PARTITIONS")),
                     replication_factor=int(os.environ.get("TOPIC_MESSAGES_BASIC_REPLICATION_FACTOR")))
    # If topic already exists, it will throw an error
    try:
        # Creating topic
        client.create_topics(new_topics=[topic], validate_only=False)
    except TopicAlreadyExistsError:
        print("Topics already set up")
        pass
    finally:
        # Close the client
        client.close()

# Init db if not existing
# Database connection function for use in routers
# And accross the REST API
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


models.Base.metadata.create_all(bind=engine)

from routes import messages, users, healthcheck, chatrooms

app.include_router(messages.router)
app.include_router(users.router)
app.include_router(healthcheck.router)
app.include_router(chatrooms.router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
