import json
from flask import request

from flask import Blueprint, render_template, session, abort

app_file3 = Blueprint('app_file3', __name__)


@app_file3.route('/fma/operations', methods=["POST"])
def invoked_operation() -> json:
    return request.data


@app_file3.route('/fma/operations/async', methods=["POST"])
def invoked_async_operation() -> json:
    return request.data
