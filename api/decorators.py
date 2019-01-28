#!/usr/bin/env python3
from functools import wraps

import jsonschema
from flask import request

from fluid_parameters import fluid_params
from hydraulic_surfaces import get_internal_diameter
from miscellaneous_tools import error_response


def json_validate(schema):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                req = request.get_json()
                jsonschema.validate(req, schema)
                return func(*args, req=req, **kwargs)
            except jsonschema.exceptions.ValidationError:
                return error_response(400, 'Missing or invalid JSON request.')

        return wrapper

    return decorator


def check_pipe_parameters(func):
    @wraps(func)
    def wrapper(req, *args, **kwargs):
        roughness = req.get('roughness', 1.5)
        internal_dimension = get_internal_diameter(req['nominal_diameter'], req['material'])
        if not internal_dimension:
            return error_response(400, 'Wrong pipe diameter value.')
        if 2 * roughness >= internal_dimension:
            return error_response(400, 'Wrong roughness value.')
        return func(*args, req=req, roughness=roughness, internal_dimension=internal_dimension, **kwargs)

    return wrapper


def get_fluid_parameters(func):
    @wraps(func)
    def wrapper(req, *args, **kwargs):
        fluid = fluid_params(req['fluid'], req['temperature'])
        density = fluid['density']
        viscosity = fluid['kinematic_viscosity']
        return func(*args, req=req, density=density, viscosity=viscosity, **kwargs)

    return wrapper
