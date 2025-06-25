"""
load_reports.py
---------------
Loads patient report data from a JSON file and inserts it into a MongoDB collection.
This script is intended for initial data population or migration.
"""

import json  # For loading JSON data
from pymongo import MongoClient  # For MongoDB connection'
import os  # For environment variable access
from dotenv import load_dotenv  # For loading environment variables from .env file

# ---------------------- MongoDB Connection ---------------------------- #
# Connect to local MongoDB instance (update URI for cloud/Atlas if needed)
# client = MongoClient(os.getenv("MONGODB_URI_KEY"))
client= MongoClient("mongodb://localhost:27017")  # Default local MongoDB URI

# Create or use the database and collection
# Change 'patient_reports_db' and 'patients' as needed for your project
db = client["patient_reports_database"]
collection = db["patients_data"]

# ---------------------- Load Data from JSON --------------------------- #
# Load patient reports from a local JSON file
with open('data/patient_reports.json') as file:
    data = json.load(file)  # `data` is a list of dicts or a single dict
    print(f"Loaded {len(data)} records from JSON file.")

# ---------------------- Insert Data into MongoDB ---------------------- #
# Insert the loaded data into the MongoDB collection
if isinstance(data, list):
    res = collection.insert_many(data)
    print(data)
else:
    res = collection.insert_one(data)

print("Data inserted successfully!")
print(res)
