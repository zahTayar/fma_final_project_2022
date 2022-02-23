import json
from flask import Blueprint, render_template, session, abort, request

from src.main.fma.controllers import operations_db

app_file3 = Blueprint('app_file3', __name__)


@app_file3.route('/fma/operations', methods=["POST"])
def invoked_operation() -> json:
    response = operations_db.insert({
        "_id": "operation_id",
        "type": "type",
        "invoked_by": "invoked_by",
        "created_timestamp": "created_timestamp",
        "operation_attributes": "operation_attributes"
    })

    return {"status": "ok", "opeartion": "success"}


@app_file3.route('/fma/operations/async', methods=["POST"])
def invoked_async_operation() -> json:
    return request.data
