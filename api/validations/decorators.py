#!/usr/bin/env python3
from functools import wraps

import jsonschema
from flask import request

from calculations.fluid_parameters import fluid_params
from calculations.hydraulic_surfaces import get_internal_diameter
from calculations.unit_convertion import unit_convertion
from response_tools.response_tools import error_response


def json_validate(schema):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            try:
                req = request.get_json()
                jsonschema.validate(req, schema)
                return func(*args, req=req, **kwargs)
            except jsonschema.exceptions.ValidationError as exc:
                return error_response(400, exc.message)

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
        if 'power' in req:
            req['temperature'] = (req['temperature_supply'] + req['temperature_return']) / 2
        fluid = fluid_params(req['fluid'], req['temperature'])
        req.update(
            {
                'density': fluid['density'],
                'specific_heat': fluid['specific_heat'],
                'viscosity': fluid['kinematic_viscosity'],
            }
        )
        return func(*args, req=req, **kwargs)

    return wrapper


def power_to_flow(func):
    @wraps(func)
    def wrapper(req, *args, **kwargs):
        if 'power' in req:
            power = unit_convertion(req['power'], req['power_unit'], 'W', 'power')
            temperature_delta = abs(req['temperature_supply'] - req['temperature_return'])
            if not temperature_delta:
                return error_response(400, 'Temperature supply and return can not have the same value.')
            flow = power / (temperature_delta * req['density'] * req['specific_heat'])
            req.update({'flow': flow, 'flow_unit': 'm3/s'})
        return func(*args, req=req, **kwargs)

    return wrapper
