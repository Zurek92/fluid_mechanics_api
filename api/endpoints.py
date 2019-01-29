#!/usr/bin/env python3
from flask import Blueprint
from flask import jsonify

from decorators import check_pipe_parameters
from decorators import get_fluid_parameters
from decorators import json_validate
from flow_equations import manning_equation
from flow_equations import velocity_equation
from headloss_equations import darcy_friction_coefficient
from headloss_equations import darcy_weisbach_equation
from headloss_equations import reynolds_equation
from hydraulic_surfaces import angle_in_partial_filled_pipe
from hydraulic_surfaces import circular_pipe
from hydraulic_surfaces import circular_water_cross_sectional_area
from hydraulic_surfaces import circular_wetted_perimeter
from hydraulic_surfaces import get_internal_diameters
from hydraulic_surfaces import hydraulic_radius
from hydraulic_surfaces import rectangular_dict
from hydraulic_surfaces import rectangular_wetted_perimeter
from json_validation_schemas import headloss_all_pipes
from json_validation_schemas import headloss_selected_pipe
from json_validation_schemas import manning_schema
from unit_convertion import unit_convertion


api = Blueprint('api', __name__)


@api.route('/health', methods=['GET'])
def health():
    """Check api health."""
    return jsonify({'status': 'everything is ok :)'})


@api.route('/calculate/headloss', methods=['POST'])
@json_validate(headloss_selected_pipe)
@check_pipe_parameters
@get_fluid_parameters
def headloss(req, roughness, internal_dimension, density, viscosity):
    """Calculate velocity and headloss for selected dimension.

    :param req: request.get_json() flask's method to get json from user
    :param roughness: roughness of pipe in [mm]
    :param internal_dimension: internal dimension of pipe depends on nominal diameter
    :param density: density of fluid [kg/m3]
    :param viscosity: viscosity of fluid [m2/s]
    """
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
    return jsonify(
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
def selecting_optimum_pipe_size(req, density, viscosity):
    """Calculate velocity and headloss for every dimension.

    :param req: request.get_json() flask's method to get json from user
    :param density: density of fluid [kg/m3]
    :param viscosity: viscosity of fluid [m2/s]
    """
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
    return jsonify({'headloss_unit': 'Pa/m', 'velocity_unit': 'm/s', 'results': results})


@api.route('/calculate/gravity_flow', methods=['POST'])
@json_validate(manning_schema)
def gravity_flow(req):
    height = req['height']
    if 'diameter' in req:
        diameter = req['diameter']
        if height > diameter:
            return jsonify({'status': 400, 'message': 'Missing or invalid JSON request.'})
        angle = angle_in_partial_filled_pipe(diameter, height)
        area = circular_water_cross_sectional_area(angle, diameter, height)
        perimeter = circular_wetted_perimeter(angle, diameter)
    else:
        width = req['width']
        area = rectangular_dict(width, height, 'm')
        perimeter = rectangular_wetted_perimeter(width, height)
    hydraulic_radius_value = hydraulic_radius(area, perimeter)
    velocity = manning_equation(hydraulic_radius_value, req['manning_coefficient'], req['slope'])
    return jsonify(
        {
            'velocity': round(velocity, 2),
            'velocity_unit': 'm/s',
            'flow': round(velocity * area * 3600, 2),
            'flow_unit': 'm3/h',
        }
    )


@api.app_errorhandler(404)
def not_found(e):
    return jsonify({'status': 404, 'message': 'not found'}), 404
