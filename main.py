from fastapi import FastAPI
from router import advertisement,user,message,transaction,rating
from db import models
from db.database import engine
from auth import authentication


app = FastAPI(title="Marketplace API")
app.include_router(user.router)
app.include_router(advertisement.router)
app.include_router(authentication.router)
app.include_router(message.router)
app.include_router(transaction.router)
app.include_router(rating.router)

#Create a database
models.Base.metadata.create_all(engine)