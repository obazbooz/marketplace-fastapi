from fastapi import FastAPI
from db import models
from db.database import engine
from router import advertisement
from auth import authentication
from router import user
from router import SearchFilter   # Added by Ali
from router import DebugAds        # Added by Prof. Ali




app = FastAPI(title="Marketplace API")
app.include_router(user.router)
app.include_router(advertisement.router)
app.include_router(authentication.router)
app.include_router(SearchFilter.router)  # Added by  Ali
app.include_router(DebugAds.router)  # Added by Prof. Ali
# @app.get("/")
# def read_root():
#     return {"status": "ok", "message": "Welcome to the Marketplace API"}


#Create a database
models.Base.metadata.create_all(engine)