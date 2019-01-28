#!/usr/bin/env python3
import jsonschema
import pytest

from json_validation_schemas import headloss_all_pipes
from json_validation_schemas import headloss_selected_pipe


@pytest.mark.parametrize(
    'json_from_user',
    (
        {'fluid': 'water', 'temperature': 20, 'material': 'steel', 'flow': 10, 'flow_unit': 'm3/h'},
        {'fluid': 'water', 'temperature': 30, 'material': 'steel', 'roughness': 1, 'flow': 10, 'flow_unit': 'm3/h'},
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
    ),
)
def test_headloss_json_from_user_failed(json_from_user):
    with pytest.raises(jsonschema.exceptions.ValidationError):
        jsonschema.validate(json_from_user, headloss_selected_pipe)
