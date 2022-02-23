from src.main.fma.controllers import users_db
from src.main.fma.data.user_entity import user_entity
from src.main.fma.boundaries.user_boundary import user_boundary
from src.main.fma.boundaries.new_user_details import new_user_details
from src.main.fma.helpers.checker_authorization import checker_authorization


class user_service:

    def __init__(self):
        self.checker = checker_authorization()

    def create_user(self, user_details):
        # check user email valid and not in db
        if not self.checker.check_valid_user(user_details.get_email()):
            raise RuntimeError("User in db")
        # check if mail null
        if not self.checker.check_email_valid(user_details.get_email()):
            raise RuntimeError("Email is not valid")
        # check if user name is null
        if not self.checker.check_user_name_valid(user_details.get_username()):
            raise RuntimeError("Username is not valid")
        user_bou = user_boundary(user_details.get_email(),
                                 user_details.get_username(),
                                 user_details.get_avatar(),
                                 user_details.get_role())
        new_user = self.convert_to_entity(user_bou)
        new_user.set_user_id(user_bou.get_email())
        users_db.insert_one(new_user.__dict__)
        return self.convert_to_boundary(new_user).__dict__

    def login(self, user_email):
        query = {"user_id": user_email}
        json = users_db.find_one(query)
        print(json)
        entity = user_entity(json['email'],json['role'],json['username'],json['avatar'],json['last_searched'])
        if not entity:
            raise RuntimeError("Email not found/exist")
        return self.convert_to_boundary(entity).__dict__

    def update_user(self, user_email, user_boundary_update):
        query = {"user_id": user_email}
        entity = users_db.find_one(query)
        if not self.checker.check_valid_user(entity.get_email()):
            raise RuntimeError("id not found")
        else:
            user_boundary_update.set_user_id(user_email)
            new_entity = self.convert_to_entity(user_boundary_update)
            users_db.insert_one(new_entity)
        return self.convert_to_boundary(new_entity).__dict__

    def delete_all_users(self, admin_email):
        query = {"user_id": admin_email}
        admin_entity = users_db.find(query)
        if not self.checker.check_valid_user(admin_entity.get_email()):
            raise RuntimeError("user not find")
        # check if the user is admin
        if not self.checker.check_admin_user(admin_entity.get_email()):
            raise RuntimeError("not autorizhed to act this operation")
        users_db.delete_many({})

    def get_all_users(self, admin_email):
        query = {"user_id": admin_email}
        admin_entity = users_db.find(query)
        if not self.checker.check_valid_user(admin_entity.get_email()):
            raise RuntimeError("user not find")
        # check if the user is admin
        if not self.checker.check_admin_user(admin_entity.get_email()):
            raise RuntimeError("not autorizhed to act this operation")
        lis = users_db.find()
        if not lis:
            raise RuntimeError("Users not found")
        return lis

    def convert_to_entity(self, user_bou):
        user = user_entity()
        user.set_avatar(user_bou.get_avatar())
        user.set_role(user_bou.get_role())
        user.set_username(user_bou.get_username())
        user.set_user_id(user_bou.get_email())
        user.set_email(user_bou.get_email())
        return user

    def convert_to_boundary(self, user_ent):
        user = user_boundary()
        user.set_avatar(user_ent.get_avatar())
        user.set_role(user_ent.get_role())
        user.set_username(user_ent.get_username())
        user.set_email(user_ent.get_user_id())
        return user
