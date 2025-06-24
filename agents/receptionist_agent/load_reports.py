import json
from pymongo import MongoClient

# from data import patient_reports # Assuming this is the correct import path      
# MongoDB connection (local)
client = MongoClient("mongodb://localhost:27017/")  # change URI if using cloud like Atlas

# Create/use database and collection
db = client["patient_reports_db"]  # change db name as needed
collection = db["patients"]

# Load data from JSON file
with open('data/patient_reports.json') as file:
    data = json.load(file)  # `data` is a list of dicts

# Insert into MongoDB
if isinstance(data, list):
    res=collection.insert_many(data)
else:
    collection.insert_one(data)

print("Data inserted successfully!")
print(res)
