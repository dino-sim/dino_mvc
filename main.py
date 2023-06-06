from fastapi import FastAPI

from db.session import Base, engine
from routers.router import api_router

app = FastAPI(title="Dino's FASTAPI Boilerplate")

Base.metadata.create_all(bind=engine)

app.include_router(api_router)
