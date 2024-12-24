# HomeMate/server/app/api/tasks.py

from flask_restful import Resource
from flask import request
from flask_jwt_extended import jwt_required
from ..custom import role_required
from ..tasks import export_to_csv


class TasksApi(Resource):
    @jwt_required()
    @role_required('Admin')
    def get(self):
        result = export_to_csv.delay()
        return {"result_id": result.id}, 200
