class user_entity:

    def __init__(self, email="", role="", username="", avatar="", user_id="", password = "", last_searched=[]):
        self.email = email
        self.role = role
        self.username = username
        self.avatar = avatar
        self.user_id = user_id
        self.password = password
        self.last_searched = last_searched


    def get_user_id(self):
        return self.user_id

    def set_user_id(self, user_id):
        self.user_id = user_id

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

    def get_password(self):
        return self.password

    def set_password(self,password):
        self.password = password