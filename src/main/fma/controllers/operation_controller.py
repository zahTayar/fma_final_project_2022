import json
from flask import Blueprint, render_template, session, abort, request
from src.main.fma.logic.operations_service import operations_service
from src.main.fma.boundaries.operation_boundary import operation_boundary
from src.main.fma.controllers import operations_db

app_file3 = Blueprint('app_file3', __name__)

service = operations_service()
@app_file3.route('/fma/operations', methods=["POST"])
def invoked_operation() -> json:
    rv = request.get_json()
    operation = operation_boundary(
        rv['_id'], rv['type'], rv['created_timestamp'],  rv['invoked_by'], rv['operation_attributes']
    )
    # response = operations_db.insert({
    #     "_id": "operation_id",
    #     "type": "type",
    #     "invoked_by": "invoked_by",
    #     "created_timestamp": "created_timestamp",
    #     "operation_attributes": "operation_attributes"
    # })

    return service.invoke_operation(boundary=operation)


@app_file3.route('/fma/operations/async', methods=["POST"])
def invoked_async_operation() -> json:
    return request.data
