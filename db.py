from pymongo import MongoClient

def get_database():
    client = MongoClient("mongodb://localhost:27017/")
    return client["hotel_db"]

if __name__ == "__main__":
    db = get_database()
    print("Conectado ao banco:", db.name)