class user_boundary():
    def __init__(self, email="", username="", avatar="", role=""):
        self.email = email
        self.username = username
        self.avatar = avatar
        self.role = role

    def get_email(self):
        return self.email

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
