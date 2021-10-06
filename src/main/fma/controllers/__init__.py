from pymongo import MongoClient

client = MongoClient("mongodb+srv://zahtayar:zah123@cluster0.1noii.mongodb.net/test")  # host uri
db = client["d"]  # Select the database
users_db = db.create_collection("Users")
items_db = db.create_collection("Items")
operations_db = db.create_collection("Operations")