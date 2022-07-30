from pymongo import MongoClient
import os
from dotenv import load_dotenv
import certifi
from cgitb import reset
from fastapi import FastAPI
from BL.trading import *
# Load .env file
load_dotenv()
# Connect to Mongo DB
connectionstring = os.environ.get(
    'ConnectionString')
client = MongoClient(str(connectionstring), tlsCAFile=certifi.where())
db = client['fsdatabase']
app = FastAPI()

# Main route


@app.get("/")
async def root():
    return {"msg": "FPI-Bitkub Bot v2"}


@app.get("/bottrade")
async def root():
    list = db.cryptobotconfig.find()
    for item in list:
        Trading(item['Name'], float(item['targetprofit']),
                float(item['targetlost']), float(item['buyprice']))
    return {"msg": "bottrade working!"}
