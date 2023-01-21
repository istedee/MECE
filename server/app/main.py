import uvicorn

from fastapi import FastAPI
from routes import messages, users

import models
from db import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(messages.router)
app.include_router(users.router)


@app.get(
    "/ping",
    tags=["health-check"],
    responses={200: {"description": "Returns 'pong' as status check msg"}},
)
async def root():
    return {"message": "pong"}


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
