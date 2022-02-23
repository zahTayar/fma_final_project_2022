class new_user_details:
    def __init__(self, email="", username="", avatar="", role="", password=""):
        self.email = email
        self.username = username
        self.avatar = avatar
        self.role = role
        self.password = password

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

    # for new password only 
    def set_new_password(self, password):
        # doing some hash for password
        self.password = password


