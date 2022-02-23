import json
from flask import Blueprint, render_template, session, abort, request
from src.main.fma.controllers import users_db
from src.main.fma.logic.user_services import user_service
from src.main.fma.boundaries.user_boundary import user_boundary
from src.main.fma.boundaries.new_user_details import new_user_details
from src.main.fma.helpers.checker_authorization import checker_authorization
from src.main.fma.data.user_role import Role
app_file4 = Blueprint('app_file4', __name__)


@app_file4.route('/fma/users/login', methods=["GET"])
def get_user_details() -> json:
    login_details={"username": request.get_json()['email'],
                   "password": request.get_json()['password']}
    service = user_service()
    return service.login(login_details)


@app_file4.route('/fma/users', methods=["POST"])
def create_new_user() -> json:
    # search if there is user with the same email
    service = user_service()
    user = new_user_details(request.get_json()["email"],
                            request.get_json()["username"],
                            request.get_json()["avatar"],
                            request.get_json()["password"],
                            Role.USER.name
                            )
    return service.create_user(user)



@app_file4.route('/fma/users/<user_email>', methods=["PUT"])
def update_user_details(user_email) -> json:
    user_details = new_user_details(request.get_json()['email'],
                                    request.get_json()['username'],
                                    request.get_json()['avatar'],
                                    request.get_json()['password'])
    service = user_service()
    return service.update_user(user_email, user_details)

