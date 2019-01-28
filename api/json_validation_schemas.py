basic_schema = {'type': 'object', 'additionalProperties': False}

basic_properties = {
    'fluid': {'type': 'string', 'enum': ['water']},
    'temperature': {'type': 'number', 'minimum': 0, 'maximum': 370, 'multipleOf': 1},
    'material': {'type': 'string', 'enum': ['steel']},
    'flow': {'type': 'number'},
    'flow_unit': {'type': 'string', 'pattern': '^(l|mm3|cm3|dm3|m3|gal)/(s|m|h)$'},
}

headloss_selected_pipe = {
    'properties': {
        'nominal_diameter': {'type': 'number'},
        'length': {'type': 'number', 'minimum': 0},
        'local_loss_coefficient': {'type': 'number', 'minimum': 0},
        'headloss_unit': {'type': 'string', 'enum': ['atm', 'Pa', 'hPa', 'kPa', 'mbar', 'bar', 'mmHg']},
        'roughness': {'type': 'number', 'minimum': 0, 'exclusiveMinimum': True},
        **basic_properties,
    },
    'required': ['fluid', 'temperature', 'nominal_diameter', 'material', 'flow', 'flow_unit', 'length'],
    **basic_schema,
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
    'required': ['fluid', 'temperature', 'material', 'flow', 'flow_unit'],
    **basic_schema,
}
