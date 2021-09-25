import json
from flask import request

from flask import Blueprint, render_template, session, abort

app_file4 = Blueprint('app_file4', __name__)


@app_file4.route('/fma/users/login/<user_email>', methods=["GET"])
def get_user_details(user_email) -> json:
    return {}


@app_file4.route('/fma/users', methods=["POST"])
def create_new_user() -> json:
    return request.data


@app_file4.route('/fma/users/<user_email>', methods=["PUT"])
def update_user_details() -> json:
    return request.data

