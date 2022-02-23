from src.main.fma.controllers import operations_db
from src.main.fma.boundaries import operation_boundary
from src.main.fma.helpers import checker_authorization
from src.main.fma.logic.operations import search
from src.main.fma.logic.operations import update_db
from src.main.fma.logic.operations import send_alert
from src.main.fma.logic.operations import display_relevent_prop
from src.main.fma.logic.operations import calculate_increase_in_value
from src.main.fma.data import operation_entity
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
        self.calculate_increase_in_value = calculate_increase_in_value()
        self.checker_authorization = checker_authorization()

    def invoke_operation(self, operation_boundary):
        # // check

        # input
        # if (!this.checker.checkOperationType(operation.getType())) {
        # throw new RuntimeException("Type can not be null or empty String");
        # }
        #
        # if (!this.checker.checkOperationItem(operation.getItem())) {
        # throw new RuntimeException("Item can not be null or empty String");
        # }
        #
        # if (!this.checker.checkOperationInvokeBy(operation.getInvokedBy())) {
        # throw new RuntimeException("User Id can not be null or empty String");
        # }



        # // check if user is present and his
        # roll = "PLAYER"
        # if (!checkerAutho.CheckPlayerUser(userSpace+'%'+email)) {
        # throw new RuntimeException("User not authorized to do this action");
        # }

        return None

    def invoke_async_operation(self, operation_boundary):
        return None

    def convert_boundary_to_entity(self, boundary):
        entity = operation_entity()
        entity.set_type(boundary.get_type())
        entity.set_active(boundary.get_active())
        entity.set_address(boundary.get_address())
        entity.set_item_attributes(boundary.get_item_attributes())
        entity.set_date_of_upload(datetime.now())
        return entity

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
        for entity in entities:
            operations.append(self.convert_entity_to_boundary(entity))
        return operations

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


