from pymongo import MongoClient
import certifi
import os
import traceback
from datetime import datetime


mongo_uri = os.getenv("MONGO_URI")
db_name = os.getenv("DB_NAME")

if not mongo_uri or not db_name:
    raise ValueError("Missing MONGO_URI or DB_NAME in environment variables.")

print("MONGO_URI from env:", mongo_uri)
print("DB_NAME from env:", db_name)

try:
    client = MongoClient(
        mongo_uri,
        tls=True,
        tlsCAFile=certifi.where()
    )
    db = client[db_name]
    collection = db["patient_diagnosis"]
    print("Connected to MongoDB successfully.")
except Exception as e:
    print(" Error connecting to MongoDB:", e)
    traceback.print_exc()
    raise e 

def save_to_mongo(data: dict) -> str | None:

    try:
        now = datetime.utcnow()
        data["timestamp"] = now.strftime("%Y-%m-%d %H:%M:%S") 
        result = collection.insert_one(data)
        print(" Data inserted with ID:", result.inserted_id)
        return str(result.inserted_id)
    except Exception as e:
        print(" Error inserting into MongoDB:", e)
        traceback.print_exc()
        return None
