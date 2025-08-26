# main.py
from fastapi import FastAPI
from db import models
from db.database import engine

from router.user import router as user_router
from router.advertisement import router as advertisement_router
from router.search_filter import router as search_filter_router
from auth import authentication

app = FastAPI(title="Marketplace API")

# register routers
app.include_router(user_router)
app.include_router(advertisement_router)
app.include_router(authentication.router)
app.include_router(search_filter_router)

# create tables if not present
models.Base.metadata.create_all(bind=engine)
