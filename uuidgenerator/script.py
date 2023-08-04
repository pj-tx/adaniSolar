import pandas as pd
import uuid

from pymongo import MongoClient

import os
from dotenv import load_dotenv
load_dotenv()

MONGO_URI = os.getenv('MONGO_URI')

# For Adani Database
def db_name():
    client = MongoClient(MONGO_URI)
    db = client["adaniSolar"]
    
    return db

db = db_name()

collection = db['survey-keys']

# Load the Excel file into a pandas DataFrame
df = pd.read_excel('Book7.xlsx', engine='openpyxl')

# Iterate over all rows in the DataFrame
for index, row in df.iterrows():
    # Extract the name, email, and phone from the row
    name = row['Employee Name']
    email = row['Primary Email']
    phone = row['Primary Phone']

    # Generate a UUID for this record
    record_id = str(uuid.uuid4())

    # Insert the record into the MongoDB collection
    collection.insert_one({
        'name': name,
        'email': email,
        'phone': phone,
        'uuid': record_id,
        "used": False,
        'country_code': "+91",
        "email_sent": 0,
        "phone_sent":0,
    })

