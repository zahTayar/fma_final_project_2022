class item_boundary:

    def __init__(self, item_id='', type='', address='', active='', date_of_upload='', item_attributes='', created_by=''):
        self.item_id = item_id
        self.type = type
        self.address = address
        self.active = active
        self.date_of_upload = date_of_upload
        self.item_attributes = item_attributes
        self.created_by = created_by

    def get_created_by(self):
        return self.created_by

    def set_created_by(self, created_by):
        self.created_by = created_by

    def get_item_id(self):
        return self.item_id

    def set_item_id(self, item_id):
        self.item_id = item_id

    def get_type(self):
        return self.type

    def set_type(self, type):
        self.type = type

    def get_address(self):
        return self.address

    def set_address(self, address):
        self.address = address

    def get_active(self):
        return self.active

    def set_active(self, active):
        self.active = active

    def get_date_of_upload(self):
        return self.date_of_upload

    def set_date_of_upload(self, date_of_upload):
        self.date_of_upload = date_of_upload

    def get_item_attributes(self):
        return self.item_attributes

    def set_item_attributes(self, item_attributes):
        self.item_attributes = item_attributes

