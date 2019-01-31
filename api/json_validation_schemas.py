basic_schema = {'type': 'object', 'additionalProperties': False}

properties_flow = {
    'flow': {'type': 'number'},
    'flow_unit': {'type': 'string', 'pattern': '^(l|mm3|cm3|dm3|m3|gal)/(s|m|h)$'},
    'temperature': {'type': 'number', 'minimum': 0, 'maximum': 370, 'multipleOf': 1},
}

properties_power = {
    'power': {'type': 'number', 'minimum': 0, 'exclusiveMinimum': True},
    'power_unit': {'type': 'string', 'enum': ['W', 'kW', 'kcal/h']},
    'temperature_supply': {'type': 'number', 'minimum': 0, 'maximum': 370, 'multipleOf': 1},
    'temperature_return': {'type': 'number', 'minimum': 0, 'maximum': 370, 'multipleOf': 1},
}

basic_properties = {
    'fluid': {'type': 'string', 'enum': ['water']},
    'material': {'type': 'string', 'enum': ['steel']},
    **properties_flow,
    **properties_power,
}

power_and_flow_required_fields = {
    'oneOf': [{'required': ['flow']}, {'required': ['power']}],
    'dependencies': {
        'flow': ['flow_unit', 'temperature'],
        'power': ['power_unit', 'temperature_supply', 'temperature_return'],
    },
}

# prepared validation schemas
headloss_selected_pipe = {
    'properties': {
        'nominal_diameter': {'type': 'number'},
        'length': {'type': 'number', 'minimum': 0},
        'local_loss_coefficient': {'type': 'number', 'minimum': 0},
        'headloss_unit': {'type': 'string', 'enum': ['atm', 'Pa', 'hPa', 'kPa', 'mbar', 'bar', 'mmHg']},
        'roughness': {'type': 'number', 'minimum': 0, 'exclusiveMinimum': True},
        **basic_properties,
    },
    'required': ['fluid', 'nominal_diameter', 'material', 'length'],
    **basic_schema,
    **power_and_flow_required_fields,
}

headloss_all_pipes = {
    'properties': {
        'roughness': {
            'type': 'number',
            'minimum': 0,
            'maximum': 4,
            'exclusiveMinimum': True,
            'exclusiveMaximum': True,
        },
        **basic_properties,
    },
    'required': ['fluid', 'material'],
    **basic_schema,
    **power_and_flow_required_fields
}

manning_schema = {
    'properties': {
        'width': {'type': 'number', 'minimum': 0, 'exclusiveMinimum': True},
        'diameter': {'type': 'number', 'minimum': 0, 'exclusiveMinimum': True},
        'height': {'type': 'number', 'minimum': 0},
        'slope': {'type': 'number', 'minimum': 0},
        'manning_coefficient': {'type': 'number', 'minimum': 0, 'exclusiveMinimum': True},
    },
    'required': ['height', 'slope', 'manning_coefficient'],
    'oneOf': [{'required': ['width']}, {'required': ['diameter']}],
    **basic_schema,
}
