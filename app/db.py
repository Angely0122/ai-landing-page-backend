from pymongo import MongoClient
from pymongo.errors import ServerSelectionTimeoutError
import os
from datetime import datetime
from bson.objectid import ObjectId

MONGO_URI = os.getenv("MONGO_URI")
if not MONGO_URI:
    raise ValueError("MONGO_URI not found in environment variables")

client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
db = client["landing_page_builder"]
pages_collection = db["pages"]

def init_db():
    """Initialize database indices"""
    try:
        # Test connection
        client.admin.command('ping')
        print("✓ MongoDB connected")
        
        # Create indices
        pages_collection.create_index("page_id", unique=True)
        pages_collection.create_index("created_at")
        pages_collection.create_index("user_id")
        print("✓ Database indices created")
    except ServerSelectionTimeoutError:
        print("✗ Failed to connect to MongoDB")
        raise

def save_page(page_spec: dict, user_id: str = None) -> dict:
    """Save page spec to MongoDB"""
    document = {
        "page_id": page_spec.get("pageId"),
        "version": page_spec.get("version", 1),
        "sections": page_spec.get("sections", []),
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow(),
        "user_id": user_id,
        "published": False
    }
    
    result = pages_collection.insert_one(document)
    document["_id"] = str(result.inserted_id)
    return document

def get_page(page_id: str) -> dict:
    """Retrieve page by ID"""
    page = pages_collection.find_one({"page_id": page_id})
    if page:
        page["_id"] = str(page["_id"])
    return page

def update_page(page_id: str, sections: list) -> dict:
    """Update page sections and increment version"""
    page = get_page(page_id)
    if not page:
        return None
    
    new_version = page.get("version", 1) + 1
    
    result = pages_collection.find_one_and_update(
        {"page_id": page_id},
        {
            "$set": {
                "sections": sections,
                "version": new_version,
                "updated_at": datetime.utcnow()
            }
        },
        return_document=True
    )
    
    if result:
        result["_id"] = str(result["_id"])
    return result

def publish_page(page_id: str) -> dict:
    """Mark page as published"""
    result = pages_collection.find_one_and_update(
        {"page_id": page_id},
        {
            "$set": {
                "published": True,
                "updated_at": datetime.utcnow()
            }
        },
        return_document=True
    )
    
    if result:
        result["_id"] = str(result["_id"])
    return result

def delete_page(page_id: str) -> bool:
    """Delete a page"""
    result = pages_collection.delete_one({"page_id": page_id})
    return result.deleted_count > 0