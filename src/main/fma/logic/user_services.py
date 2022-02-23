from src.main.fma.controllers import users_db
from src.main.fma.data.user_entity import user_entity
from src.main.fma.boundaries.user_boundary import user_boundary


class user_service:

    def __init__(self):
        pass

    def create_user(self, user_bou):
        # check user email valid and not in db
        # check if mail null
        # check if user name is null
        new_user = self.convert_to_entity(user_bou)
        new_user.set_user_id(user_boundary.get_email())
        users_db.insert_one(new_user)
        return self.convert_to_boundary(new_user)

    def login(self, user_email):
        query = {"user_id": user_email}
        entity = users_db.find(query)
        if not entity:
            raise RuntimeError("id not found")
        else:
            return self.convert_to_boundary(entity)

    def update_user(self, user_email, user_boundary_update):
        query = {"user_id": user_email}
        entity = users_db.find(query)
        if not entity:
            raise RuntimeError("id not found")
        else:
            user_boundary_update.set_user_id(user_email)
            new_entity = self.convert_to_entity(user_boundary_update)
            users_db.insert_one(new_entity)

    def delete_all_users(self, admin_email):
        query = {"user_id": admin_email}
        admin_entity = users_db.find(query)
        if not admin_entity:
            raise RuntimeError("user not find")
        # check if the user is admin
        if not admin_entity.get_role() == "admin":
            raise RuntimeError("not autorizhed to act this operation")
        users_db.delete_many({})

    def get_all_users(self, admin_email):
        query = {"user_id": admin_email}
        admin_entity = users_db.find(query)
        if not admin_entity:
            raise RuntimeError("user not find")
        # check if the user is admin
        if not admin_entity.get_role() == "admin":
            raise RuntimeError("not autorizhed to act this operation")
        lis = users_db.find()
        if not lis:
            raise RuntimeError("Users not found")
        return lis

    def convert_to_entity(self, user_bou):
        user = user_entity()
        user.set_avatar(user_bou.get_avatar)
        user.set_role(user_bou.get_role)
        user.set_username(user_bou.get_username)
        user.set_user_id(user_bou.get_email)
        return user

    def convert_to_boundary(self, user_ent):
        user = user_boundary()
        user.set_avatar(user_ent.get_avatar)
        user.set_role(user_ent.get_role)
        user.set_username(user_ent.get_username)
        user.set_user_id(user_ent.get_email)
        return user
