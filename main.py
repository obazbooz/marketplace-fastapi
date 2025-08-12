from fastapi import FastAPI
from db import models
from db.database import engine
from router import advertisement

app = FastAPI(title="Marketplace API")
app.include_router(advertisement.router)

@app.get("/")
def read_root():
    return {"status": "ok", "message": "Welcome to the Marketplace backend app"}


#Create a database
models.Base.metadata.create_all(engine)