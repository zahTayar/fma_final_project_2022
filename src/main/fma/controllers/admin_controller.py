import json
from flask import request
from flask import Blueprint
app_file1 = Blueprint('app_file1', __name__)
from src.main.fma.logic.item_service import item_service
from src.main.fma.logic.user_services import user_service
from src.main.fma.logic.operations_service import operation_service


@app_file1.route('/fma/admin/users/<user_email>', methods=["GET"])
def get_all_users(user_email) -> json:
    return user_service().get_all_users(user_email)


@app_file1.route('/fma/admin/operations/<user_email>', methods=["GET"])
def get_all_operations(user_email) -> json:
    return operation_service.get_all_operations(user_email)


@app_file1.route('/fma/admin/users/<user_email>', methods=["DELETE"])
def delete_all_users(user_email):
    return user_service().delete_all_users(user_email)


@app_file1.route('/fma/admin/items/<user_email>', methods=["DELETE"])
def delete_all_items(user_email):
    return item_service.delete_all_items(user_email)


@app_file1.route('/fma/admin/operations/<user_email>', methods=["DELETE"])
def delete_all_operations(user_email):
    return operation_service.delete_all_operation(user_email)
