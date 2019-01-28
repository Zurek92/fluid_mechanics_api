#!/usr/bin/env python3
from flask import Blueprint
from flask import jsonify

from decorators import check_pipe_parameters
from decorators import json_validate
from fluid_parameters import fluid_params
from flow_equations import velocity_equation
from headloss_equations import darcy_friction_coefficient
from headloss_equations import darcy_weisbach_equation
from headloss_equations import reynolds_equation
from hydraulic_surfaces import circular_pipe
from hydraulic_surfaces import get_internal_diameters
from json_validation_schemas import headloss_all_pipes
from json_validation_schemas import headloss_selected_pipe
from unit_convertion import unit_convertion


api = Blueprint('api', __name__)


@api.route('/health', methods=['GET'])
def health():
    """Check api health."""
    return jsonify({'status': 'everything is ok :)'})


@api.route('/calculate/headloss', methods=['POST'])
@json_validate(headloss_selected_pipe)
@check_pipe_parameters
def headloss(req, roughness, internal_dimension):
    # fluid parameters
    fluid = fluid_params(req['fluid'], req['temperature'])
    density = fluid['density']
    viscosity = fluid['kinematic_viscosity']
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
def selecting_optimum_pipe_size(req):
    # fluid parameters
    fluid = fluid_params(req['fluid'], req['temperature'])
    density = fluid['density']
    viscosity = fluid['kinematic_viscosity']
    # pipe
    roughness = req.get('roughness', 1.5)
    # every iteration
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


@api.app_errorhandler(404)
def not_found(e):
    return jsonify({'status': 404, 'message': 'not found'}), 404
