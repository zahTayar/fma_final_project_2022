from pymongo import MongoClient
client = MongoClient("mongodb+srv://zahtayar:zah123@cluster0.1noii.mongodb.net/test")  # host uri
db = client["d"]  # Select the database
users_db = db.get_collection("Users")
operations_db = db.get_collection("Operations")
items_db = db.get_collection("Items")

if not users_db:
    users_db = db.create_collection("Users")

if not operations_db:
    operations_db = db.create_collection("Operations")

if not items_db:
    items_db = db.create_collection("Items")

