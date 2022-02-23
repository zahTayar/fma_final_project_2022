from src.main.fma.controllers import users_db
from src.main.fma.data import user_entity
from src.main.fma.data.user_role import

class checker_autorization:
    def __init__(self):
        pass

    def check_email_valid(self, email_string):
        if not email_string.contains('@'):
            return False

    def check_valid_user(self, id_string):
        query = {"user_id": id_string}
        entity=users_db.find(query)
        if not entity:
            return False
        else:
            return True

    def check_admin_user(self, id_string):
        query = {"user_id": id_string}
        entity = users_db.find(query)
        if not entity:
            if entity.get_role() == user_role.ADMIN:
                return False
            else:
                return True