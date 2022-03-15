from src.main.fma.controllers import operations_db
from src.main.fma.boundaries.operation_boundary import operation_boundary
from src.main.fma.helpers.checker_authorization import checker_authorization
from src.main.fma.logic.operations.search import search
from src.main.fma.logic.operations.send_alert import send_alert
from src.main.fma.logic.operations.calculate_increase_in_value import calculate_incrase_in_value
from src.main.fma.data.operation_entity import operation_entity
import pymongo.errors as mongodb_errors
from datetime import datetime
import uuid


# object  invokeOperation (operationBoundary)
# operationBoundary  invokeAsyncOperation (operationBoundary)
# List <operationBoundary> getAllOperations (adminEmail)
# void deleteAllOperations (adminEmail)

class operations_service:
    def __init__(self):
        self.search = search()
        self.send_alert = send_alert()
        self.calculate_increase_in_value = calculate_incrase_in_value()
        self.checker_authorization = checker_authorization()

    def invoke_operation(self, boundary):
        entity = self.convert_boundary_to_entity(boundary)
        entity.set_operation_id(str(uuid.uuid4()))
        operations_db.insert(entity.__dict__)

        if boundary.get_type() == 'search':
            return self.search.search_apartment(boundary.get_operation_attributes()["item_id"]).__dict__

        if boundary.get_type() == 'search_apartments_data':
            rv = self.search.search_previous_apartment_data(boundary.get_operation_attributes()["item_id"]).__dict__
            print(rv)
            return rv

        if boundary.get_type() == 'send_alert':
            self.send_alert.send_alert()
            return self.convert_entity_to_boundary(entity).__dict__

        if boundary.get_type() == 'calculate_increase_in_value':
            return self.calculate_increase_in_value.calculate_increase_in_value(
                boundary.get_operation_attributes()["asset_room_numebers"],
                boundary.get_operation_attributes()["asset_size_in_meters"],
                boundary.get_operation_attributes()["location"])

    def invoke_async_operation(self, boundary):
        return None

    def convert_boundary_to_entity(self, boundary):
        entity = operation_entity()
        entity.set_type(boundary.get_type())
        entity.set_operation_attributes(boundary.get_operation_attributes())
        entity.set_invoked_by(boundary.get_invoked_by())
        entity.set_created_timestamp(datetime.now().strftime("%d/%m/%Y, %H:%M:%S"))
        return entity

    def convert_entity_to_boundary(self, entity):
        boundary = operation_boundary()
        boundary.set_operation_id(entity.get_operation_id())
        boundary.set_type(entity.get_type())
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
