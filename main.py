from fastapi import FastAPI
from db import models
from db.database import engine
from router import advertisement
from auth import authentication
from router import user


app = FastAPI(title="Marketplace API")
app.include_router(user.router)
app.include_router(advertisement.router)
app.include_router(authentication.router)


# @app.get("/")
# def read_root():
#     return {"status": "ok", "message": "Welcome to the Marketplace API"}


#Create a database
models.Base.metadata.create_all(engine)