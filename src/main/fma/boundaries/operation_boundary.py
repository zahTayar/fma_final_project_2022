import uuid
class operation_boundary:

    def __init__(self, operation_id, type, created_timestamp,invoked_by, operation_attributes):
        self.operation_id = operation_id + str(uuid.uuid4()) ;
        self.type = type;
        self.created_timestamp = created_timestamp;
        self.invoked_by = invoked_by;
        self.operation_attributes = dict(operation_attributes);

    def get_operation_id(self):
        return self.operation_id;

    def get_type(self):
        return self.type;

    def get_created_timestamp(self):
        return self.created_timestamp;

    def get_operation_attributes(self):
        return self.operation_attributes;

    def get_invoked_by(self):
        return self.invoked_by;

    def set_operation_attributes(self, operation_attributes):
        self.operation_attributes = operation_attributes;
