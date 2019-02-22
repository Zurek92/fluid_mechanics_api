#!/usr/bin/env python3
from flask import Blueprint

from calculations.flow_equations import manning_equation, velocity_equation
from calculations.headloss_equations import darcy_friction_coefficient, darcy_weisbach_equation, reynolds_equation
from calculations.hydraulic_surfaces import (
    angle_in_partial_filled_pipe,
    circular_pipe,
    circular_water_cross_sectional_area,
    circular_wetted_perimeter,
    get_internal_diameters,
    hydraulic_radius,
    rectangular_dict,
    rectangular_wetted_perimeter,
)
from calculations.unit_convertion import unit_convertion
from response_tools.response_tools import api_response, error_response
from validations.decorators import check_pipe_parameters, get_fluid_parameters, json_validate, power_to_flow
from validations.json_validation_schemas import headloss_all_pipes, headloss_selected_pipe, manning_schema


api = Blueprint('api', __name__)


@api.route('/health', methods=['GET'])
def health():
    """Check api health."""
    return api_response({'status': 'everything is ok :)'})


@api.route('/calculate/headloss', methods=['POST'])
@json_validate(headloss_selected_pipe)
@check_pipe_parameters
@get_fluid_parameters
@power_to_flow
def headloss(req, roughness, internal_dimension):
    """Calculate velocity and headloss for selected dimension.

    :param req: request.get_json() flask's method to get json from user
    :param roughness: roughness of pipe in [mm]
    :param internal_dimension: internal dimension of pipe depends on nominal diameter
    """
    density = req['density']
    viscosity = req['viscosity']
    # pipe
    area = circular_pipe(internal_dimension, 'mm')
    length = req['length']
    llc = req.get('local_loss_coefficient', 0)
    # flow
    velocity = velocity_equation(req['flow'], req['flow_unit'], area)
    reynolds = reynolds_equation(velocity, internal_dimension, viscosity)
    # headloss
    headloss_unit = req.get('headloss_unit', 'Pa')
    dfc = darcy_friction_coefficient(reynolds, internal_dimension, roughness)
    loss = darcy_weisbach_equation(
        dfc, llc, length, unit_convertion(internal_dimension, 'mm', 'm', 'lenght'), density, velocity
    )
    return api_response(
        {
            'velocity': velocity,
            'velocity_unit': 'm/s',
            'headloss': unit_convertion(loss, 'Pa', headloss_unit, 'pressure'),
            'headloss_unit': headloss_unit,
        }
    )


@api.route('/calculate/pipes', methods=['POST'])
@json_validate(headloss_all_pipes)
@get_fluid_parameters
@power_to_flow
def selecting_optimum_pipe_size(req):
    """Calculate velocity and headloss for every dimension.

    :param req: request.get_json() flask's method to get json from user
    """
    density = req['density']
    viscosity = req['viscosity']
    roughness = req.get('roughness', 1.5)
    results = []
    for nominal_diameter, internal_dimension in get_internal_diameters(req['material']):
        area = circular_pipe(internal_dimension, 'mm')
        velocity = velocity_equation(req['flow'], req['flow_unit'], area)
        reynolds = reynolds_equation(velocity, internal_dimension, viscosity)
        dfc = darcy_friction_coefficient(reynolds, internal_dimension, roughness)
        loss = darcy_weisbach_equation(
            dfc, 0, 1, unit_convertion(internal_dimension, 'mm', 'm', 'lenght'), density, velocity
        )
        results.append({'nominal_diameter': nominal_diameter, 'headloss': loss, 'velocity': velocity})
    return api_response({'headloss_unit': 'Pa/m', 'velocity_unit': 'm/s', 'results': results})


@api.route('/calculate/gravity_flow', methods=['POST'])
@json_validate(manning_schema)
def gravity_flow(req):
    """Calculate gravity flow and velocity.

    :param req: request.get_json() flask's method to get json from user
    """
    height = req['height']
    if 'diameter' in req:
        diameter = req['diameter']
        if height > diameter:
            return error_response(400, 'Missing or invalid JSON request.')
        angle = angle_in_partial_filled_pipe(diameter, height)
        area = circular_water_cross_sectional_area(angle, diameter, height)
        perimeter = circular_wetted_perimeter(angle, diameter)
    else:
        width = req['width']
        area = rectangular_dict(width, height, 'm')
        perimeter = rectangular_wetted_perimeter(width, height)
    hydraulic_radius_value = hydraulic_radius(area, perimeter)
    velocity = manning_equation(hydraulic_radius_value, req['manning_coefficient'], req['slope'])
    return api_response(
        {
            'velocity': round(velocity, 2),
            'velocity_unit': 'm/s',
            'flow': round(velocity * area * 3600, 2),
            'flow_unit': 'm3/h',
        }
    )


@api.app_errorhandler(404)
def not_found(e):
    return error_response(404, 'not found')


@api.app_errorhandler(405)
def wrong_method(e):
    return error_response(405, 'wrong method')
