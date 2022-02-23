import pymongo.errors as mongodb_errors
from bson import json_util

from src.main.fma.controllers import items_db
from src.main.fma.boundaries.item_boundary import item_boundary
from src.main.fma.helpers.checker_authorization import checker_authorization
from src.main.fma.data.item_entity import item_entity
from datetime import datetime
import uuid
import json


class item_service:

    def __init__(self):
        self.checker_authorization = checker_authorization()

    def get_specific_item(self, item_id):
        rv = {}
        try:
            rv = items_db.find_one({"item_id": item_id})
        except mongodb_errors:
            print(str(mongodb_errors))
        entity = item_entity(
            rv['item_id'], rv['type'], rv['address'], rv['active'], rv['date_of_upload'], rv['item_attributes'], rv['created_by']
        )
        return self.convert_entity_to_boundary(entity).__dict__

    def create_item(self, boundary):
        entity = self.convert_boundary_to_entity(boundary)
        entity.set_item_id(str(uuid.uuid4()))
        items_db.insert(entity.__dict__)
        return self.convert_entity_to_boundary(entity).__dict__

    def convert_entity_to_boundary(self, entity):
        boundary = item_boundary()
        boundary.set_item_id(entity.get_item_id())
        boundary.set_type(entity.get_type())
        boundary.set_item_attributes(entity.get_item_attributes())
        boundary.set_address(entity.get_address())
        boundary.set_active(entity.get_active())
        boundary.set_date_of_upload(entity.get_date_of_upload())
        boundary.set_created_by(entity.get_created_by())
        return boundary

    def convert_boundary_to_entity(self, boundary):
        entity = item_entity()
        entity.set_type(boundary.get_type())
        entity.set_active(boundary.get_active())
        entity.set_address(boundary.get_address())
        entity.set_item_attributes(boundary.get_item_attributes())
        entity.set_date_of_upload(datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
        entity.set_created_by(boundary.get_created_by())
        return entity

    def update_item(self, item_id, boundary):
        my_query = {"item_id": item_id}
        nv = dict()
        nv['address'] = boundary.get_address()
        nv['active'] = boundary.get_active()
        nv['item_attributes'] = boundary.get_item_attributes()
        new_values = {"$set": nv}
        try:
            items_db.update_one(my_query, new_values)
        except mongodb_errors:
            print(str(mongodb_errors))
        return boundary.__dict__

    def delete_all_items(self, user_email):
        # check auth of user_email
        if not self.checker_authorization.check_admin_user(user_email):
            raise RuntimeError("not autorizhed to act this operation")
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
            entities = items_db.find({"created_by": user_email})
        except mongodb_errors:
            print(str(mongodb_errors))
        for rv in entities:
            items.append(
                item_boundary(rv['item_id'], rv['type'], rv['address'], rv['active'], rv['date_of_upload'], rv['item_attributes'],
                              rv['created_by']))
        my_dict = dict()
        for index, value in enumerate(items):
            my_dict[index] = value.__dict__
        return my_dict
