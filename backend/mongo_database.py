"""
mongo_database.py
-----------------
Provides MongoDB connection and helper functions for retrieving patient records by name or ID.
Loads configuration from environment variables or uses defaults for local development.
"""

# ---------------------- Environment Setup ----------------------------- #
from pymongo import MongoClient  # MongoDB client
from dotenv import load_dotenv  # For loading .env files
import os  # For environment variable access

load_dotenv()  # Load environment variables from .env file

# ---------------------- MongoDB Configuration ------------------------- #
# MONGO_URI = os.getenv("MONGODB_URI_KEY")  # MongoDB URI from environment variable
MONGO_URI = "mongodb://localhost:27017"  # Default local MongoDB URI
DB_NAME = "patient_reports_database"  # Database name
COLLECTION_NAME = "patients_data"  # Collection name

# ---------------------- MongoDB Client/Collection --------------------- #
client = MongoClient(MONGO_URI)
collection = client[DB_NAME][COLLECTION_NAME]

# ---------------------- Patient Query Functions ----------------------- #
def get_patient_by_name(name):
    """
    Retrieve a patient record by name (case-insensitive, exact match).
    Args:
        name (str): Patient's full name.
    Returns:
        dict: Patient record if found.
        str: 'multiple' if multiple matches found.
        None: If no match found.
    """
    matches = list(collection.find({"patient_name": {"$regex": f"^{name}$", "$options": "i"}}))
    if not matches:
        return None
    elif len(matches) > 1:
        return "multiple"
    return matches[0]

def get_patient_by_id(patient_id):
    """
    Retrieve a patient record by patient ID.
    Args:
        patient_id (str): Unique patient identifier.
    Returns:
        dict: Patient record if found, else None.
    """
    match = collection.find_one({"patient_id": patient_id})
    if not match:
        return None
    return match

print(get_patient_by_id("P001"))  # Example usage to test connection and query