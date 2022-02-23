import json
from flask import request
from flask import Blueprint, render_template, session, abort
from src.main.fma.controllers import db
app_file1 = Blueprint('app_file1', __name__)
from src.main.fma.logic.item_service import item_service
from src.main.fma.logic.user_services import user_service


@app_file1.route('/fma/admin/users/<user_email>', methods=["GET"])
def get_all_users(user_email) -> json:
    return db.get_collection("Users")


@app_file1.route('/fma/admin/operations/<user_email>', methods=["GET"])
def get_all_operations(user_email) -> json:
    if "@" not in user_email:
        return {}
    dic = {"1": "one", "2": "two"}  # suppose to be dictionary of all users
    return dic


@app_file1.route('/fma/admin/users/<user_email>', methods=["DELETE"])
def delete_all_users(user_email):
    return f'Hello {user_email}'


@app_file1.route('/fma/admin/items/<user_email>', methods=["DELETE"])
def delete_all_items(user_email):
    return f'Hello {user_email}'


@app_file1.route('/fma/admin/operations/<user_email>', methods=["DELETE"])
def delete_all_operations(user_email):
    return f'Hello {user_email}'
