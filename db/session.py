from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from odmantic import AIOEngine
import boto3

import os

load_dotenv()

db_user = os.environ.get('DB_USER')
db_pwd = os.environ.get('DB_PASSWORD')
db_host = os.environ.get('DB_HOST')
db_port = os.environ.get('DB_PORT')
db_database = os.environ.get('DB_DATABASE')

SQL_ALCHEMY_DATABASE_URL = f"mysql+pymysql://{db_user}:{db_pwd}@{db_host}:{db_port}/{db_database}?charset=utf8"
engine = create_engine(SQL_ALCHEMY_DATABASE_URL, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
#
mongo_host = os.environ.get('MONGO_HOST')
mongo_port = os.environ.get('MONGO_PORT')
mongo_database = os.environ.get('MONGO_DATABASE')


# mongo_client = motor.motor_asyncio.AsyncIOMotorClient(f"mongodb://{mongo_host}:{mongo_port}/{mongo_database}")


class MongoDB:
    def __init__(self):
        self.client = None

    def connect(self):
        self.client = AsyncIOMotorClient(f"mongodb://{mongo_host}:{mongo_port}/{mongo_database}")
        self.engine = AIOEngine(client=self.client, database=mongo_database)
        print("MongoDB Connect Success!")

    def close(self):
        self.client.close()


s3_access_key = os.environ.get('S3_ACCESS_KEY')
s3_secret_key = os.environ.get('S3_SECRET_KEY')

client_s3 = boto3.client(
    's3',
    aws_access_key_id=s3_access_key,
    aws_secret_access_key=s3_secret_key
)

Base = declarative_base()
mongodb = MongoDB()
