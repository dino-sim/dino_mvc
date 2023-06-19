from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from db.session import Base, engine, mongodb
from routers.router import api_router

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app = FastAPI(title="Dino's FASTAPI Boilerplate")

Base.metadata.create_all(bind=engine)


# db = mongo_client.college

@app.on_event("startup")
def on_app_start():
    mongodb.connect()


@app.on_event("shutdown")
async def on_app_shutdown():
    mongodb.close()


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router)
