from flask import request
import json
from flask import Blueprint
from src.main.fma.logic.item_service import item_service
from src.main.fma.boundaries.item_boundary import item_boundary

app_file2 = Blueprint('app_file2', __name__)
item_service = item_service()


@app_file2.route('/fma/items/<user_email>', methods=["POST"])
def get_items_of_specific_search_by_user(user_email) -> json:
    return item_service.get_all_items(user_email)


@app_file2.route('/fma/items/<item_id>', methods=["GET"])
def get_specific_item(item_id) -> json:
    return item_service.get_specific_item(item_id)


@app_file2.route('/fma/items/store', methods=["POST"])
def store_item() -> json:
    rv = request.get_json()
    item = item_boundary(
        rv['item_id'], rv['type'], rv['address'], rv['active'], '', rv['item_attributes'], rv['created_by']
    )
    return item_service.create_item(item)


@app_file2.route('/fma/items/<item_id>', methods=["PUT"])
def update_item(item_id) -> json:
    rv = request.get_json()
    item = item_boundary(
        rv['item_id'], rv['type'], rv['address'], rv['active'], '', rv['item_attributes'], rv['created_by']
    )
    return item_service.update_item(item_id, item)
