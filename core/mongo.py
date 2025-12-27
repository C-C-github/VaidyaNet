from pymongo import MongoClient

# MongoDB Atlas connection
client = MongoClient(
    "mongodb+srv://satkurikailash_db_user:LXQ70z9WCLeX25o8@cluster0.dbizlsl.mongodb.net/healthcare_db"
)

# Database
db = client["healthcare_db"]

# Collection (THIS WAS MISSING OR MISNAMED)
medical_records = db["medical_records"]
audit_logs = db["audit_logs"]
