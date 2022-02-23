class user_entity:

    def __init__(self, email="", role="", username="", avatar="", _id="", last_searched=[], password=""):
        self.email = email
        self.role = role
        self.username = username
        self.avatar = avatar
        self._id = _id
        self.last_searched = last_searched
        self.password = password

    def get_pass(self):
        return self.password

    def set_password(self, password):
        self.password = password

    def get_user_id(self):
        return self._id

    def set_user_id(self, _id):
        self._id = _id

    def get_role(self):
        return self.role

    def set_role(self, role):
        self.role = role

    def get_username(self):
        return self.username

    def set_username(self, username):
        self.username = username

    def get_avatar(self):
        return self.avatar

    def set_avatar(self, avatar):
        self.avatar = avatar

    def get_email(self):
        return self.email

    def set_email(self, email):
        self.email=email
