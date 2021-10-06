import json
from flask import Blueprint, render_template, session, abort, request
from src.main.fma.controllers import users_db

app_file4 = Blueprint('app_file4', __name__)


@app_file4.route('/fma/users/login/<user_email>', methods=["GET"])
def get_user_details(user_email) -> json:
    dic = {
        "_id": user_email
    }

    res = users_db.find_one(dic)
    if res is None:
        return {"message": "user not found please check your speling", "status": "200 OK"}
    return res


@app_file4.route('/fma/users', methods=["POST"])
def create_new_user() -> json:
    # search if there is user with the same email
    response = users_db.insert({
        "_id": request.get_json()["email"],
        "role": request.get_json()["role"],
        "username": request.get_json()["username"],
        "avatar": request.get_json()["avatar"],
    })
    return {"status": "ok", "opeartion": "success"}


@app_file4.route('/fma/users/<user_email>', methods=["PUT"])
def update_user_details() -> json:
    # create from details json
    new_user_details_to_update = {
        "_id": request.get_json()["email"],
        "role": request.get_json()["role"],
        "username": request.get_json()["username"],
        "avatar": request.get_json()["avatar"],
    }
    # just id to verify exist
    just_id = {"_id": request.get_json()["email"]}
    res = users_db.find_one(just_id)
    if res is None:
        return {"message": "user not found please check your speling", "status": "200 OK"}
    else:
        # verify again and update
        users_db.find_one_and_update(just_id, new_user_details_to_update)
    return {"status": "ok", "opeartion": "success"}
