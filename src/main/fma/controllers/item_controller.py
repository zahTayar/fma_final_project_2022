
from flask import request
import json
from flask import Blueprint, render_template, session, abort

app_file2 = Blueprint('app_file2', __name__)
@app_file2.route('/fma/items/<user_email>', methods=["POST"])
def get_items_of_specific_search_by_user(user_email) -> json:
    return request.data


@app_file2.route('/fma/items/<user_email>/<item_id>', methods=["GET"])
def get_specific_item(user_email, item_id) -> json:
    return {}


@app_file2.route('/fma/items/store/<user_email>', methods=["POST"])
def store_item(user_email) -> json:
    return request.data


@app_file2.route('/fma/items/<user_email>/<item_id>', methods=["PUT"])
def update_item(user_email, item_id) -> json:
    return request.data
