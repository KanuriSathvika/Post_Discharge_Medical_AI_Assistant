from pymongo import MongoClient
from dotenv import load_dotenv
import os

load_dotenv()

MONGO_URI = os.getenv("mongodb://localhost:27017")  # e.g., mongodb://localhost:27017
DB_NAME = "patient_reports_db"
COLLECTION_NAME = "patients"

client = MongoClient(MONGO_URI)
collection = client[DB_NAME][COLLECTION_NAME]

def get_patient_by_name(name):
    matches = list(collection.find({"patient_name": {"$regex": f"^{name}$", "$options": "i"}}))
    if not matches:
        return None
    elif len(matches) > 1:
        return "multiple"
    return matches[0]

def get_patient_by_id(patient_id):
    match= collection.find_one({"patient_id": patient_id})
    if not match:
        return None
    return match