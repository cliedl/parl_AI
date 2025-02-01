import os
from datetime import datetime, timedelta, timezone

import dotenv
from bson import ObjectId
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

dotenv.load_dotenv()


def add_log_dict(dictionary: dict) -> str:
    """
    Log a dictionary to the database and return the inserted id.
    Args:
        dictionary: The dictionary to log.
    Returns:
        The inserted id.
    """
    # Add timestamp to dictionary
    dictionary["created_at"] = datetime.now(timezone.utc) + timedelta(
        hours=1
    )  # Berlin timezone (UTC+1)

    client = MongoClient(os.getenv("MONGODB_URI"), server_api=ServerApi("1"))
    db = client[os.getenv("DATABASE_NAME")]
    collection = db[os.getenv("COLLECTION_NAME")]
    result = collection.insert_one(dictionary)
    return result.inserted_id


def update_log_dict(_id: str, dictionary: dict):
    """
    Update a dictionary in the database.
    Args:
        _id: The id of the dictionary to update.
        dictionary: The dictionary to update.
    Returns:
        The result of the update.
    """
    # Add updated_at timestamp to dictionary
    dictionary["updated_at"] = datetime.now(timezone.utc) + timedelta(hours=1)

    client = MongoClient(os.getenv("MONGODB_URI"), server_api=ServerApi("1"))
    db = client[os.getenv("DATABASE_NAME")]
    collection = db[os.getenv("COLLECTION_NAME")]
    result = collection.update_one(
        filter={"_id": ObjectId(_id)}, update={"$set": dictionary}
    )
    return result


if __name__ == "__main__":
    _id = add_log_dict({"query": "What?", "answer": "test", "rating": "10"})
    print(_id)
    result = update_log_dict(_id, {"answer": "test2"})
    print(type(result))
