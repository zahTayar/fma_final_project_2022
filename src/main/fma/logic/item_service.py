import pymongo.errors as mongodb_errors
from src.main.fma.controllers import items_db
from src.main.fma.boundaries.item_boundary import item_boundary
from src.main.fma.data.item_entity import item_entity
from datetime import datetime
import uuid


class item_service:

    def get_specific_item(self, item_id):
        entity = {}
        try:
            entity = items_db.find({"item_id": item_id})
        except mongodb_errors:
            print(str(mongodb_errors))
        return self.convert_entity_to_boundary(entity)

    def create_item(self, boundary):
        # check input
        entity = self.convert_boundary_to_entity(boundary)
        entity.set_item_id(str(uuid.uuid4()))
        return self.convert_entity_to_boundary(items_db.insert_one(entity))

    def convert_entity_to_boundary(self, entity):
        boundary = item_boundary()
        boundary.set_item_id(entity.get_item_id())
        boundary.set_type(entity.get_type())
        boundary.set_item_attributes(entity.get_item_attributes())
        boundary.set_address(entity.get_address())
        boundary.set_active(entity.get_active())
        boundary.set_date_of_upload(entity.get_date_of_upload())
        return boundary

    def convert_boundary_to_entity(self, boundary):
        entity = item_entity()
        entity.set_type(boundary.get_type())
        entity.set_active(boundary.get_active())
        entity.set_address(boundary.get_address())
        entity.set_item_attributes(boundary.get_item_attributes())
        entity.set_date_of_upload(datetime.now())
        return entity

    def update_item(self, item_id, boundary):
        my_query = {"item_id": item_id}
        new_values = {"$set": self.convert_boundary_to_entity(boundary)}
        try:
            items_db.update_one(my_query, new_values)
        except mongodb_errors:
            print(str(mongodb_errors))

    def delete_all_items(self, user_email):
        # check auth of user_email
        x = []
        try:
            x = items_db.delete_many({})
        except mongodb_errors:
            print(str(mongodb_errors))
        print(x.deleted_count, " documents deleted.")

    def get_all_items(self, user_email):
        # check auth of user_email
        items = []
        entities = []
        try:
            entities = items_db.find()
        except mongodb_errors:
            print(str(mongodb_errors))
        for entity in entities:
            items.append(self.convert_entity_to_boundary(entity))
        return items
