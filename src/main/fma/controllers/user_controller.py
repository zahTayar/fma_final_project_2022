import json

import flask
from flask import Blueprint, render_template, session, abort, request
from src.main.fma.controllers import users_db
from src.main.fma.logic.user_services import user_service
from src.main.fma.boundaries.user_boundary import user_boundary
from src.main.fma.boundaries.new_user_details import new_user_details
from src.main.fma.helpers.checker_authorization import checker_authorization

app_file4 = Blueprint('app_file4', __name__)


@app_file4.route('/fma/users/login/<user_email>', methods=["GET"])
def get_user_details(user_email) -> json:
    dic = {
        "_id": user_email
    }
    service = user_service()
    res = service.login(user_email)
    d = flask.jsonify(res)
    d.headers.add('Access-Control-Allow-Origin', '*')
    return d


@app_file4.route('/fma/users', methods=["POST"])
def create_new_user() -> json:
    # search if there is user with the same email
    service = user_service()
    user = new_user_details(request.get_json()["email"],
                            request.get_json()["username"],
                            request.get_json()["avatar"],
                            request.get_json()["role"],
                            request.get_json()["password"])
    return  service.create_user(user)



@app_file4.route('/fma/users/<user_email>', methods=["PUT"])
def update_user_details(user_email) -> json:
    # create from details json
    new_user_details_to_update = {
        "_id": request.get_json()["email"],
        "role": request.get_json()["role"],
        "username": request.get_json()["username"],
        "avatar": request.get_json()["avatar"],
    }
    # just id to verify exist
    just_id = {"_id": user_email}
    res = users_db.find(just_id)
    if res is None:
        return {"message": "user not found please check your speling", "status": "200 OK"}
    else:
        # verify again and update
        users_db.update_one(just_id, new_user_details_to_update)
    return {"status": "ok", "opeartion": "success"}
