import uvicorn

from fastapi import FastAPI

import models
from db import engine, SessionLocal

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


models.Base.metadata.create_all(bind=engine)

from routes import messages, users, healthcheck

app.include_router(messages.router)
app.include_router(users.router)
app.include_router(healthcheck.router)


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
