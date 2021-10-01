
class user_entity:

    def __init__(self, email, role, username, avatar):
        self.email = email
        self.role = role
        self.username = username
        self.avatar = avatar

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
