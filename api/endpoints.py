#!/usr/bin/env python3
from flask import Blueprint
from flask import jsonify
from flask import request

from fluid_parameters import fluid_params
from flow_equations import velocity_equation
from headloss_equations import darcy_friction_coefficient
from headloss_equations import darcy_weisbach_equation
from headloss_equations import reynolds_equation
from hydraulic_surfaces import circular_pipe
from hydraulic_surfaces import get_internal_diameter
from unit_convertion import unit_convertion


api = Blueprint('api', __name__)


@api.route('/health', methods=['GET'])
def health():
    """Check api health."""
    return jsonify({'status': 'everything is ok :)'})


@api.route('/calculate/headloss', methods=['POST'])
def headloss():
    req = request.get_json()
    # fluid parameters
    fluid = fluid_params(req['fluid'], req['temperature'])
    density = fluid['density']
    viscosity = fluid['kinematic_viscosity']
    # pipe
    internal_dimension = get_internal_diameter(req['nominal_diameter'], req['material'])
    area = circular_pipe(internal_dimension, 'mm')
    roughness = req.get('roughness', 1.5)
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
