from flask import request
import json
from flask import Blueprint, render_template, session, abort
from src.main.fma.logic.item_service import item_service

app_file2 = Blueprint('app_file2', __name__)


@app_file2.route('/fma/items/<user_email>', methods=["POST"])
def get_items_of_specific_search_by_user(user_email) -> json:
    return item_service.get_all_items(user_email)


@app_file2.route('/fma/items/<user_email>/<item_id>', methods=["GET"])
def get_specific_item(user_email, item_id) -> json:
    return item_service.get_specific_item(user_email, item_id)


@app_file2.route('/fma/items/store/<user_email>', methods=["POST"])
def store_item(user_email) -> json:
    # response = items_db.insert({
    #     "_id": request.get_json()["_id"],
    #     "type": request.get_json()["type"],
    #     "address": request.get_json()["address"],
    #     "active": request.get_json()["active"],
    #     "date_of_upload": request.get_json()["date_of_upload"],
    #     "item_attributes": request.get_json()["item_attributes"]
    # })
    return item_service.create_item(user_email, request.get_json())


@app_file2.route('/fma/items/<user_email>/<item_id>', methods=["PUT"])
def update_item(user_email, item_id) -> json:
    return item_service.update_item(user_email, item_id, request.get_json())
