#!/usr/bin/env python3
import jsonschema
import pytest

from json_validation_schemas import headloss_all_pipes
from json_validation_schemas import headloss_selected_pipe
from json_validation_schemas import manning_schema


@pytest.mark.parametrize(
    'json_from_user',
    (
        {'fluid': 'water', 'temperature': 20, 'material': 'steel', 'flow': 10, 'flow_unit': 'm3/h'},
        {'fluid': 'water', 'temperature': 30, 'material': 'steel', 'roughness': 1, 'flow': 10, 'flow_unit': 'm3/h'},
        {
            'fluid': 'water',
            'temperature_supply': 60,
            'temperature_return': 40,
            'material': 'steel',
            'power': 10,
            'power_unit': 'kW',
        },
    ),
)
def test_headloss_all_pipes(json_from_user):
    jsonschema.validate(json_from_user, headloss_all_pipes)


@pytest.mark.parametrize(
    'json_from_user',
    (
        # wrong fluid name
        {'fluid': 'water123', 'temperature': 20, 'material': 'steel', 'flow': 10, 'flow_unit': 'm3/h'},
        # wrong fluid type
        {'fluid': 12, 'temperature': 30, 'material': 'steel', 'flow': 10, 'flow_unit': 'm3/h'},
        # wrong temperature value
        {'fluid': 'water', 'temperature': -20, 'material': 'steel', 'flow': 10, 'flow_unit': 'm3/h'},
        # wrong temperature type
        {'fluid': 'water', 'temperature': 'nnn', 'material': 'steel', 'flow': 10, 'flow_unit': 'm3/h'},
        # wrong material name
        {'fluid': 'water', 'temperature': 20, 'material': 'steel11', 'flow': 10, 'flow_unit': 'm3/h'},
        # wrong material type
        {'fluid': 'water', 'temperature': 20, 'material': 12, 'flow': 10, 'flow_unit': 'm3/h'},
        # wrong flow type
        {'fluid': 'water', 'temperature': 20, 'material': 'steel', 'flow': 'zzz', 'flow_unit': 'm3/h'},
        # wrong flow_unit type
        {'fluid': 'water', 'temperature': 20, 'material': 'steel', 'flow': 10, 'flow_unit': 12},
        # wrong flow_unit value
        {'fluid': 'water', 'temperature': 20, 'material': 'steel', 'flow': 10, 'flow_unit': 'm3/hz'},
        # wrong roughness value
        {'fluid': 'water', 'temperature': 20, 'material': 'steel', 'flow': 10, 'flow_unit': 'm3/h', 'roughness': 10},
        # missing fluid parameter
        {'temperature': 20, 'material': 'steel', 'flow': 10, 'flow_unit': 'm3/h'},
        # missing temperature parameter
        {'fluid': 'water', 'material': 'steel', 'flow': 10, 'flow_unit': 'm3/h'},
        # missing material parameter
        {'fluid': 'water', 'temperature': 20, 'flow': 10, 'flow_unit': 'm3/h'},
        # missing flow parameter
        {'fluid': 'water', 'temperature': 20, 'material': 'steel', 'flow_unit': 'm3/h'},
        # missing flow_unit parameter
        {'fluid': 'water', 'temperature': 20, 'material': 'steel', 'flow': 10},
        # missing temperature_supply
        {'fluid': 'water', 'material': 'steel', 'power': 10, 'power_unit': 'W', 'temperature_return': 50},
        # missing temperature_return
        {'fluid': 'water', 'material': 'steel', 'power': 10, 'power_unit': 'W', 'temperature_supply': 50},
        # missing power_unit
        {'fluid': 'water', 'material': 'steel', 'power': 10, 'temperature_return': 50, 'temperature_supply': 60},
        # wrong temperature_supply type
        {
            'fluid': 'water',
            'temperature_supply': 'zzz',
            'temperature_return': 40,
            'material': 'steel',
            'power': 10,
            'power_unit': 'kW',
        },
        # wrong temperature_supply value
        {
            'fluid': 'water',
            'temperature_supply': -40,
            'temperature_return': 40,
            'material': 'steel',
            'power': 10,
            'power_unit': 'kW',
        },
        # wrong temperature_return type
        {
            'fluid': 'water',
            'temperature_supply': 40,
            'temperature_return': 'zz',
            'material': 'steel',
            'power': 10,
            'power_unit': 'kW',
        },
        # wrong temperature_return value
        {
            'fluid': 'water',
            'temperature_supply': 40,
            'temperature_return': -40,
            'material': 'steel',
            'power': 10,
            'power_unit': 'kW',
        },
        # wrong power type
        {
            'fluid': 'water',
            'temperature_supply': 60,
            'temperature_return': 40,
            'material': 'steel',
            'power': 'zz',
            'power_unit': 'kW',
        },
        # wrong power value
        {
            'fluid': 'water',
            'temperature_supply': 60,
            'temperature_return': 40,
            'material': 'steel',
            'power': 0,
            'power_unit': 'kW',
        },
        # wrong power_unit value
        {
            'fluid': 'water',
            'temperature_supply': 60,
            'temperature_return': 40,
            'material': 'steel',
            'power': 0,
            'power_unit': 'kWa',
        },
    ),
)
def test_headloss_all_pipes_failed(json_from_user):
    with pytest.raises(jsonschema.exceptions.ValidationError):
        jsonschema.validate(json_from_user, headloss_all_pipes)


@pytest.mark.parametrize(
    'json_from_user',
    (
        {
            'fluid': 'water',
            'temperature': 30,
            'nominal_diameter': 25,
            'material': 'steel',
            'flow': 10,
            'flow_unit': 'm3/h',
            'length': 10,
        },
        {
            'fluid': 'water',
            'temperature': 30,
            'nominal_diameter': 25,
            'material': 'steel',
            'flow': 10,
            'flow_unit': 'm3/h',
            'length': 10,
            'roughness': 1.5,
        },
        {
            'fluid': 'water',
            'temperature': 30,
            'nominal_diameter': 25,
            'material': 'steel',
            'flow': 10,
            'flow_unit': 'm3/h',
            'length': 10,
            'roughness': 1.5,
            'local_loss_coefficient': 15,
        },
        {
            'fluid': 'water',
            'temperature': 30,
            'nominal_diameter': 25,
            'material': 'steel',
            'flow': 10,
            'flow_unit': 'm3/h',
            'length': 10,
            'roughness': 1.5,
            'local_loss_coefficient': 15,
            'headloss_unit': 'kPa',
        },
        {
            'fluid': 'water',
            'temperature_supply': 70,
            'temperature_return': 50,
            'nominal_diameter': 25,
            'material': 'steel',
            'power': 10,
            'power_unit': 'W',
            'length': 10,
            'roughness': 1.5,
            'local_loss_coefficient': 15,
            'headloss_unit': 'kPa',
        },
    ),
)
def test_headloss_json_from_user(json_from_user):
    jsonschema.validate(json_from_user, headloss_selected_pipe)


@pytest.mark.parametrize(
    'json_from_user',
    (
        # wrong fluid name
        {
            'fluid': 'water1',
            'temperature': 30,
            'nominal_diameter': 25,
            'material': 'steel',
            'flow': 10,
            'flow_unit': 'm3/h',
            'length': 10,
        },
        # wrong fluid type
        {
            'fluid': 12,
            'temperature': 30,
            'nominal_diameter': 25,
            'material': 'steel',
            'flow': 10,
            'flow_unit': 'm3/h',
            'length': 10,
        },
        # wrong temperature type
        {
            'fluid': 'water',
            'temperature': '30',
            'nominal_diameter': 25,
            'material': 'steel',
            'flow': 10,
            'flow_unit': 'm3/h',
            'length': 10,
        },
        # wrong temperature value
        {
            'fluid': 'water',
            'temperature': 666,
            'nominal_diameter': 25,
            'material': 'steel',
            'flow': 10,
            'flow_unit': 'm3/h',
            'length': 10,
        },
        # wrong temperature, not multiple of 1
        {
            'fluid': 'water',
            'temperature': 30.5,
            'nominal_diameter': 25,
            'material': 'steel',
            'flow': 10,
            'flow_unit': 'm3/h',
            'length': 10,
        },
        # wrong nominal_diameter type
        {
            'fluid': 'water',
            'temperature': 30,
            'nominal_diameter': '25',
            'material': 'steel',
            'flow': 10,
            'flow_unit': 'm3/h',
            'length': 10,
        },
        # wrong material type
        {
            'fluid': 'water',
            'temperature': 30,
            'nominal_diameter': 25,
            'material': 12,
            'flow': 10,
            'flow_unit': 'm3/h',
            'length': 10,
        },
        # wrong material value
        {
            'fluid': 'water',
            'temperature': 30,
            'nominal_diameter': 25,
            'material': 'steel1',
            'flow': 10,
            'flow_unit': 'm3/h',
            'length': 10,
        },
        # wrong flow type
        {
            'fluid': 'water',
            'temperature': 30,
            'nominal_diameter': 25,
            'material': 'steel',
            'flow': '10',
            'flow_unit': 'm3/h',
            'length': 10,
        },
        # wrong flow_unit type
        {
            'fluid': 'water',
            'temperature': 30,
            'nominal_diameter': 25,
            'material': 'steel',
            'flow': 10,
            'flow_unit': 12,
            'length': 10,
        },
        # wrong flow_unit value (volume)
        {
            'fluid': 'water',
            'temperature': 30,
            'nominal_diameter': 25,
            'material': 'steel',
            'flow': 10,
            'flow_unit': 'm/h',
            'length': 10,
        },
        # wrong flow_unit value (time)
        {
            'fluid': 'water',
            'temperature': 30,
            'nominal_diameter': 25,
            'material': 'steel',
            'flow': 10,
            'flow_unit': 'm3/z',
            'length': 10,
        },
        # wrong length type
        {
            'fluid': 'water',
            'temperature': 30,
            'nominal_diameter': 25,
            'material': 'steel',
            'flow': 10,
            'flow_unit': 'm3/h',
            'length': '10',
        },
        # wrong length value
        {
            'fluid': 'water',
            'temperature': 30,
            'nominal_diameter': 25,
            'material': 'steel',
            'flow': 10,
            'flow_unit': 'm3/h',
            'length': -10,
        },
        # wrong roughness type
        {
            'fluid': 'water',
            'temperature': 30,
            'nominal_diameter': 25,
            'material': 'steel',
            'flow': 10,
            'flow_unit': 'm3/h',
            'length': 10,
            'roughness': '1',
        },
        # wrong roughness value
        {
            'fluid': 'water',
            'temperature': 30,
            'nominal_diameter': 25,
            'material': 'steel',
            'flow': 10,
            'flow_unit': 'm3/h',
            'length': 10,
            'roughness': 0,
        },
        # wrong local_loss_coefficient type
        {
            'fluid': 'water',
            'temperature': 30,
            'nominal_diameter': 25,
            'material': 'steel',
            'flow': 10,
            'flow_unit': 'm3/h',
            'length': 10,
            'local_loss_coefficient': '1',
        },
        # wrong local_loss_coefficient value
        {
            'fluid': 'water',
            'temperature': 30,
            'nominal_diameter': 25,
            'material': 'steel',
            'flow': 10,
            'flow_unit': 'm3/h',
            'length': 10,
            'local_loss_coefficient': -1,
        },
        # wrong headloss_unit type
        {
            'fluid': 'water',
            'temperature': 30,
            'nominal_diameter': 25,
            'material': 'steel',
            'flow': 10,
            'flow_unit': 'm3/h',
            'length': 10,
            'headloss_unit': 12,
        },
        # wrong headloss_unit value
        {
            'fluid': 'water',
            'temperature': 30,
            'nominal_diameter': 25,
            'material': 'steel',
            'flow': 10,
            'flow_unit': 'm3/h',
            'length': 10,
            'headloss_unit': 'atm1',
        },
        # missing fluid parameter
        {
            'temperature': 30,
            'nominal_diameter': 25,
            'material': 'steel',
            'flow': 10,
            'flow_unit': 'm3/h',
            'length': 10,
        },
        # missing temperature parameter
        {
            'fluid': 'water',
            'nominal_diameter': 25,
            'material': 'steel',
            'flow': 100,
            'flow_unit': 'dm3/s',
            'length': 100,
        },
        # missing nominal_diameter parameter
        {
            'fluid': 'water',
            'temperature': 30,
            'material': 'steel',
            'flow': 1000,
            'flow_unit': 'dm3/s',
            'length': 100000,
        },
        # missing material parameter
        {
            'fluid': 'water',
            'temperature': 30,
            'nominal_diameter': 25,
            'flow': 1000,
            'flow_unit': 'dm3/h',
            'length': 1000,
        },
        # missing flow parameter
        {
            'fluid': 'water',
            'temperature': 30,
            'nominal_diameter': 25,
            'material': 'steel',
            'flow_unit': 'm3/h',
            'length': 10,
        },
        # missing flow_unit parameter
        {
            'fluid': 'water',
            'temperature': 30,
            'nominal_diameter': 25,
            'material': 'steel',
            'flow': 10000,
            'length': 10000,
        },
        # missing length parameter
        {
            'fluid': 'water',
            'temperature': 30,
            'nominal_diameter': 25,
            'material': 'steel',
            'flow': 10,
            'flow_unit': 'm3/h',
        },
        # missing power
        {
            'fluid': 'water',
            'nominal_diameter': 25,
            'material': 'steel',
            'length': 10,
            'power_unit': 'kW',
            'temperature_supply': 70,
            'temperature_return': 50,
        },
        # wrong power type
        {
            'fluid': 'water',
            'nominal_diameter': 25,
            'material': 'steel',
            'length': 10,
            'power': 'zz',
            'power_unit': 'kW',
            'temperature_supply': 70,
            'temperature_return': 50,
        },
        # wrong power value
        {
            'fluid': 'water',
            'nominal_diameter': 25,
            'material': 'steel',
            'length': 10,
            'power': 0,
            'power_unit': 'kW',
            'temperature_supply': 70,
            'temperature_return': 50,
        },
        # missing power_unit
        {
            'fluid': 'water',
            'nominal_diameter': 25,
            'material': 'steel',
            'length': 10,
            'power': 10,
            'temperature_supply': 70,
            'temperature_return': 50,
        },
        # wrong power_unit type
        {
            'fluid': 'water',
            'nominal_diameter': 25,
            'material': 'steel',
            'length': 10,
            'power': 10,
            'power_unit': 12,
            'temperature_supply': 70,
            'temperature_return': 50,
        },
        # wrong power_unit value
        {
            'fluid': 'water',
            'nominal_diameter': 25,
            'material': 'steel',
            'length': 10,
            'power': 10,
            'power_unit': 'kWs',
            'temperature_supply': 70,
            'temperature_return': 50,
        },
        # missing temperature_supply
        {
            'fluid': 'water',
            'nominal_diameter': 25,
            'material': 'steel',
            'length': 10,
            'power': 10,
            'power_unit': 'kW',
            'temperature_return': 50,
        },
        # wrong temperature_supply type
        {
            'fluid': 'water',
            'nominal_diameter': 25,
            'material': 'steel',
            'length': 10,
            'power': 10,
            'power_unit': 'kW',
            'temperature_supply': 'zz',
            'temperature_return': 50,
        },
        # wrong temperature_supply value
        {
            'fluid': 'water',
            'nominal_diameter': 25,
            'material': 'steel',
            'length': 10,
            'power': 10,
            'power_unit': 'kW',
            'temperature_supply': -40,
            'temperature_return': 50,
        },
        # missing temperature_return
        {
            'fluid': 'water',
            'nominal_diameter': 25,
            'material': 'steel',
            'length': 10,
            'power': 10,
            'power_unit': 'kW',
            'temperature_supply': 70,
        },
        # wrong temperature_return type
        {
            'fluid': 'water',
            'nominal_diameter': 25,
            'material': 'steel',
            'length': 10,
            'power': 10,
            'power_unit': 'kW',
            'temperature_supply': 70,
            'temperature_return': 'zz',
        },
        # wrong temperature_return value
        {
            'fluid': 'water',
            'nominal_diameter': 25,
            'material': 'steel',
            'length': 10,
            'power': 10,
            'power_unit': 'kW',
            'temperature_supply': 70,
            'temperature_return': -50,
        },
    ),
)
def test_headloss_json_from_user_failed(json_from_user):
    with pytest.raises(jsonschema.exceptions.ValidationError):
        jsonschema.validate(json_from_user, headloss_selected_pipe)


@pytest.mark.parametrize(
    'json_from_user',
    (
        {'width': 1, 'height': 1, 'slope': 0.01, 'manning_coefficient': 0.013},
        {'diameter': 1, 'height': 1, 'slope': 0.01, 'manning_coefficient': 0.013},
    ),
)
def test_manning_schema(json_from_user):
    jsonschema.validate(json_from_user, manning_schema)


@pytest.mark.parametrize(
    'json_from_user',
    (
        # width and diameter in one json
        {'width': 1, 'diameter': 1, 'height': 1, 'slope': 0.01, 'manning_coefficient': 0.013},
        # wrong diameter/width type
        {'diameter': 'z', 'height': 1, 'slope': 0.01, 'manning_coefficient': 0.013},
        {'width': 'z', 'height': 1, 'slope': 0.01, 'manning_coefficient': 0.013},
        # wrong diameter/width value
        {'diameter': -1, 'height': 1, 'slope': 0.01, 'manning_coefficient': 0.013},
        {'width': -1, 'height': 1, 'slope': 0.01, 'manning_coefficient': 0.013},
        {'diameter': 0, 'height': 1, 'slope': 0.01, 'manning_coefficient': 0.013},
        {'width': 0, 'height': 1, 'slope': 0.01, 'manning_coefficient': 0.013},
        # wrong height type
        {'diameter': 1, 'height': 'z', 'slope': 0.01, 'manning_coefficient': 0.013},
        # wrong height value
        {'diameter': 1, 'height': -1, 'slope': 0.01, 'manning_coefficient': 0.013},
        # wrong slope type
        {'diameter': 1, 'height': 1, 'slope': 'z', 'manning_coefficient': 0.013},
        # wrong slope value
        {'diameter': 1, 'height': 1, 'slope': -0.01, 'manning_coefficient': 0.013},
        # wrong coefficient type
        {'diameter': 1, 'height': 1, 'slope': 0.01, 'manning_coefficient': 'z'},
        # wrong coefficient value
        {'diameter': 1, 'height': 1, 'slope': 0.01, 'manning_coefficient': -0.013},
        {'diameter': 1, 'height': 1, 'slope': 0.01, 'manning_coefficient': 0},
        # missing width and diameter
        {'height': 1, 'slope': 0.01, 'manning_coefficient': 0.013},
        # missing height
        {'diameter': 1, 'slope': 0.01, 'manning_coefficient': 0.013},
        # missing slope
        {'diameter': 1, 'height': 1, 'manning_coefficient': 0.013},
        # missing coefficient
        {'diameter': 1, 'height': 1, 'slope': 0.01},
    ),
)
def test_manning_schema_failed(json_from_user):
    with pytest.raises(jsonschema.exceptions.ValidationError):
        jsonschema.validate(json_from_user, manning_schema)
