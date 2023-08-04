from pymongo import MongoClient

import os
from dotenv import load_dotenv
load_dotenv()

MONGO_URI = os.getenv('MONGO_URI')

# For JD Database
def db_name():
    client = MongoClient(MONGO_URI)
    db = client["adaniSolar"]
    
    return db