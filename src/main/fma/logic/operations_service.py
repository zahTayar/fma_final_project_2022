from src.main.fma.controllers import operations_db
from src.main.fma.controllers import items_db


from src.main.fma.boundaries import operation_boundary
from src.main.fma.helpers import checker_authorization
from src.main.fma.logic.operations import search
from src.main.fma.logic.operations import update_db
from src.main.fma.logic.operations import send_alert
from src.main.fma.logic.operations import display_relevent_prop
from src.main.fma.logic.operations import calculate_increase_in_value




        # object  invokeOperation (operationBoundary)
		# operationBoundary  invokeAsyncOperation (operationBoundary)
		# List <operationBoundary> getAllOperations (adminEmail)
		# void deleteAllOperations (adminEmail)
class operation_service :
    def __init__(self, search,update_db,send_alert,display_relevent_prop,calculate_incrase_in_value):
        self.search = search
        self.update_db = update_db
        self.send_alert = send_alert
        self.display_relevent_prop = display_relevent_prop
        self.calculate_incrase_in_value = calculate_incrase_in_value

    def invoke_operation (self,operation_boundary):
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


        email = operation_boundary.get_invoked_by(self);

        # // check if user is present and his
        # roll = "PLAYER"
        # if (!checkerAutho.CheckPlayerUser(userSpace+'%'+email)) {
        # throw new RuntimeException("User not authorized to do this action");
        # }



        return None
    def invoke_async_operation (self,operation_boundary):
        return None

    def get_all_operations(self,admin_email):
        if checker_authorization:
            operations_db.find()


        return None
    def delete_all_operation(self,admin_email):
        if checker_authorization :
            operations_db.delete_many({})














