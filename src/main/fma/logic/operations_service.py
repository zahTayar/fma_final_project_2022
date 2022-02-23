from src.main.fma.controllers import operations_db
from src.main.fma.boundaries.operation_boundary import operation_boundary
from src.main.fma.helpers.checker_authorization import checker_authorization
from src.main.fma.logic.operations.search import search
from src.main.fma.logic.operations.update_db import update_db
from src.main.fma.logic.operations.send_alert import send_alert
from src.main.fma.logic.operations.display_relevent_prop import display_relevent_prop
from src.main.fma.logic.operations.calculate_increase_in_value import calculate_incrase_in_value
from src.main.fma.data.operation_entity import operation_entity
import pymongo.errors as mongodb_errors
from datetime import datetime
import uuid


# object  invokeOperation (operationBoundary)
# operationBoundary  invokeAsyncOperation (operationBoundary)
# List <operationBoundary> getAllOperations (adminEmail)
# void deleteAllOperations (adminEmail)

class operation_service:
    def __init__(self):
        self.search = search()
        self.update_db = update_db()
        self.send_alert = send_alert()
        self.display_relevent_prop = display_relevent_prop()
        self.calculate_increase_in_value = calculate_incrase_in_value()
        self.checker_authorization = checker_authorization()

    def invoke_operation(self, boundary):

        entity = self.convert_boundary_to_entity(boundary)

        if boundary.get_type == 'search':
            self.search.search()
            entity.set_operation_id(str(uuid.uuid4()))
            operations_db.insert(entity.__dict__)
        if boundary.get_type == 'update_db':
            self.update_db.update_db()
            entity.set_operation_id(str(uuid.uuid4()))
            operations_db.insert(entity.__dict__)
        if boundary.get_type == 'send_alert':
            self.send_alert.send_alert()
            entity.set_operation_id(str(uuid.uuid4()))
            operations_db.insert(entity.__dict__)
        if boundary.get_type == 'display_relevent_prop':
            self.display_relevent_prop.display_relevent_prop()
            entity.set_operation_id(str(uuid.uuid4()))
            operations_db.insert(entity.__dict__)
        if boundary.get_type == 'calculate_increase_in_value':
            self.calculate_increase_in_value.calculate_increase_in_value()
            entity.set_operation_id(str(uuid.uuid4()))
            operations_db.insert(entity.__dict__)

    def invoke_async_operation(self, boundary):
        return None

    def convert_boundary_to_entity(self, boundary):
        entity = operation_entity()
        entity.set_type(boundary.get_type())
        entity.set_operation_attributes(boundary.get_operation_attributes())
        entity.set_invoked_by(boundary.get_invoked_by())
        entity.set_created_timestamp(datetime.now().strftime("%m/%d/%Y, %H:%M:%S"))
        return entity

    def convert_entity_to_boundary(self, entity):
        boundary = operation_boundary()
        boundary.set_operation_id(entity.get_operation_id())
        boundary.set_type(entity.set_type())
        boundary.set_operation_attributes(entity.get_operation_attributes())
        boundary.set_invoked_by(entity.get_invoked_by())
        boundary.set_created_timestamp(entity.get_created_timestamp())
        return boundary

    def get_all_operations(self, admin_email):
        # check auth of admin_email
        if not self.checker_authorization.check_admin_user(admin_email):
            raise RuntimeError("not autorizhed to act this operation")
        operations = []
        entities = []
        try:
            entities = operations_db.find()
        except mongodb_errors:
            print(str(mongodb_errors))
        for rv in entities:
            operations.append(
                operation_boundary(rv['operation_id'], rv['type'], rv['invoked_by'], rv['created_timestamp'],
                                   rv['operation_attributes']))
        my_dict = dict()
        for index, value in enumerate(operations):
            my_dict[index] = value.__dict__
        return my_dict

    def delete_all_operation(self, admin_email):
        # check auth of admin_email
        if not self.checker_authorization.check_admin_user(admin_email):
            raise RuntimeError("not autorizhed to act this operation")
        x = []
        try:
            x = operations_db.delete_many({})
        except mongodb_errors:
            print(str(mongodb_errors))
        print(x.deleted_count, " documents deleted.")
