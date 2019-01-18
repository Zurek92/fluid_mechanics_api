#!/usr/bin/env python3
from flask import Blueprint
from flask_restful import Api
from flask_restful import Resource

api_endpoints = Blueprint('api', __name__)
api = Api(api_endpoints)


class Health(Resource):
    """Check api health."""

    def get(self):
        return {'status': 'everything is ok :)'}


api.add_resource(Health, '/health')
