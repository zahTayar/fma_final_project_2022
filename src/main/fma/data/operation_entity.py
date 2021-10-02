class operation_entity:
    def __init__(self, operation_id, type, created_timestamp, operation_attributes):
        self.operation_id = operation_id;
        self.type = type;
        self.created_timestamp = created_timestamp;
        self.operation_attributes = operation_attributes;

    def get_operation_id(self):
        return self.operation_id;

    def get_type(self):
        return self.type;

    def get_created_timestamp(self):
        return self.created_timestamp;

    def get_operation_attributes(self):
        return self.operation_attributes;

    def set_operation_attributes(self, operation_attributes):
        self.operation_attributes = operation_attributes;
