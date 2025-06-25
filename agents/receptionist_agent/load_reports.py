"""
load_reports.py
---------------
Loads patient report data from a JSON file and inserts it into a MongoDB collection.
This script is intended for initial data population or migration.
"""

import json  # For loading JSON data
from pymongo import MongoClient  # For MongoDB connection

# ---------------------- MongoDB Connection ---------------------------- #
# Connect to local MongoDB instance (update URI for cloud/Atlas if needed)
client = MongoClient("mongodb://localhost:27017/")

# Create or use the database and collection
# Change 'patient_reports_db' and 'patients' as needed for your project
db = client["patient_reports_db"]
collection = db["patients"]

# ---------------------- Load Data from JSON --------------------------- #
# Load patient reports from a local JSON file
with open('data/patient_reports.json') as file:
    data = json.load(file)  # `data` is a list of dicts or a single dict

# ---------------------- Insert Data into MongoDB ---------------------- #
# Insert the loaded data into the MongoDB collection
if isinstance(data, list):
    res = collection.insert_many(data)
else:
    res = collection.insert_one(data)

print("Data inserted successfully!")
print(res)
