from pymongo import MongoClient
client = MongoClient("mongodb+srv://zahtayar:zah123@cluster0.1noii.mongodb.net/test")  # host uri
db = client["d"]  # Select the database
users_db = db.get_collection("Users")
operations_db = db.get_collection("Operations")
items_db = db.get_collection("Items")
yad_2_db = db.get_collection("apartments")
nadlan_gov_db = db.get_collection("apartments_data")

if not users_db:
    users_db = db.create_collection("Users")

if not operations_db:
    operations_db = db.create_collection("Operations")

if not items_db:
    items_db = db.create_collection("Items")

if not yad_2_db:
    yad_2_db = db.create_collection("yad_2_apartments")

if not nadlan_gov_db:
    nadlan_gov_db = db.create_collection("apartments_data")