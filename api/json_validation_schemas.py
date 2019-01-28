headloss_json_from_user = {
    'type': 'object',
    'properties': {
        'fluid': {'type': 'string', 'enum': ['water']},
        'temperature': {'type': 'number', 'minimum': 0, 'maximum': 370, 'multipleOf': 1},
        'nominal_diameter': {'type': 'number'},
        'material': {'type': 'string', 'enum': ['steel']},
        'flow': {'type': 'number'},
        'flow_unit': {'type': 'string', 'pattern': '^(l|mm3|cm3|dm3|m3|gal)/(s|m|h)$'},
        'length': {'type': 'number', 'minimum': 0},
        'roughness': {'type': 'number', 'minimum': 0, 'exclusiveMinimum': True},
        'local_loss_coefficient': {'type': 'number', 'minimum': 0},
        'headloss_unit': {'type': 'string', 'enum': ['atm', 'Pa', 'hPa', 'kPa', 'mbar', 'bar', 'mmHg']},
    },
    'additionalProperties': False,
    'required': ['fluid', 'temperature', 'nominal_diameter', 'material', 'flow', 'flow_unit', 'length'],
}
