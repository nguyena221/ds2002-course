import os 
from pymongo import MongoClient

MONGODB_ATLAS_URL = os.getenv("MONGODB_ATLAS_URL")
MONGODB_ATLAS_USER = os.getenv("MONGODB_ATLAS_USER")
MONGODB_ATLAS_PWD = os.getenv("MONGODB_ATLAS_PWD")

def main():
    url = f"mongodb+srv://{MONGODB_ATLAS_USER}:{MONGODB_ATLAS_PWD}@{MONGODB_ATLAS_URL}"
    
    client = MongoClient(url)
    db = client["bookstore"]
    authors = db["authors"]

    total = authors.count_documents({})
    
    print("Title: Bookstore Authors")
    print(f"Total authors: {total}")
    print()

    for i in authors.find({}).sort("name",1):
        name = i["name"]
        nationality = i["nationality"]
        print(f"{name} - {nationality}")

    client.close()
    
if __name__ == "__main__":
    main()