#!/usr/bin/env python3
import pytest

from main import app


@pytest.fixture()
def app_fixture():
    app.config['TESTING'] = True
    client = app.test_client()
    yield client


def test_health_endpoint(app_fixture):
    resp = app_fixture.get('/health')
    assert resp.status_code == 200
    assert resp.get_json() == {'status': 'everything is ok :)'}


@pytest.mark.parametrize(
    'req_json, expected_resp',
    (
        (
            {
                'fluid': 'water',
                'temperature': 30,
                'nominal_diameter': 25,
                'material': 'steel',
                'flow': 1,
                'flow_unit': 'm3/h',
                'length': 10,
            },
            {'velocity': 0.48, 'velocity_unit': 'm/s', 'headloss': 3163, 'headloss_unit': 'Pa'},
        ),
        (
            {
                'fluid': 'water',
                'temperature': 30,
                'nominal_diameter': 25,
                'material': 'steel',
                'flow': 1,
                'flow_unit': 'm3/h',
                'length': 10,
                'headloss_unit': 'kPa',
            },
            {'velocity': 0.48, 'velocity_unit': 'm/s', 'headloss': 3.163, 'headloss_unit': 'kPa'},
        ),
        (
            {
                'fluid': 'water',
                'temperature': 30,
                'nominal_diameter': 25,
                'material': 'steel',
                'flow': 1,
                'flow_unit': 'm3/h',
                'length': 10,
                'local_loss_coefficient': 15,
                'headloss_unit': 'kPa',
            },
            {'velocity': 0.48, 'velocity_unit': 'm/s', 'headloss': 4.883, 'headloss_unit': 'kPa'},
        ),
        (
            {
                'fluid': 'water',
                'temperature': 30,
                'nominal_diameter': 25,
                'material': 'steel',
                'flow': 1,
                'flow_unit': 'm3/h',
                'length': 10,
                'roughness': 1,
                'local_loss_coefficient': 15,
                'headloss_unit': 'kPa',
            },
            {'velocity': 0.48, 'velocity_unit': 'm/s', 'headloss': 4.335, 'headloss_unit': 'kPa'},
        ),
    ),
)
def test_headloss_endpoint(app_fixture, req_json, expected_resp):
    resp = app_fixture.post('/calculate/headloss', json=req_json)
    assert resp.get_json() == expected_resp


@pytest.mark.parametrize(
    'req_json, message',
    (
        (None, 'Missing or invalid JSON request.'),
        (
            {
                'fluid': 'water',
                'temperature': 30,
                'nominal_diameter': 25,
                'material': 'steel',
                'flow': 10,
                'flow_unit': 'm3/h',
                'length': -1,
            },
            'Missing or invalid JSON request.',
        ),
        (
            {
                'fluid': 'water',
                'temperature': 30,
                'nominal_diameter': 25,
                'roughness': 20,
                'material': 'steel',
                'flow': 10,
                'flow_unit': 'm3/h',
                'length': 1,
            },
            'Wrong roughness value.',
        ),
        (
            {
                'fluid': 'water',
                'temperature': 30,
                'nominal_diameter': 24,
                'material': 'steel',
                'flow': 10,
                'flow_unit': 'm3/h',
                'length': 1,
            },
            'Wrong pipe diameter value.',
        ),
    ),
)
def test_headloss_endpoint_failed(app_fixture, req_json, message):
    resp = app_fixture.post('/calculate/headloss', json=req_json)
    assert resp.get_json() == {'status': 400, 'message': message}


@pytest.mark.parametrize(
    'req_json, expected_resp',
    (
        (
            {
                'fluid': 'water',
                'temperature': 20,
                'material': 'steel',
                'roughness': 1.5,
                'flow': 10,
                'flow_unit': 'm3/h',
            },
            {
                'headloss_unit': 'Pa/m',
                'velocity_unit': 'm/s',
                'results': [
                    {'nominal_diameter': 8, 'headloss': 16561320, 'velocity': 45.67},
                    {'nominal_diameter': 10, 'headloss': 2312644, 'velocity': 22.64},
                    {'nominal_diameter': 15, 'headloss': 583861, 'velocity': 13.82},
                    {'nominal_diameter': 20, 'headloss': 111520, 'velocity': 7.58},
                    {'nominal_diameter': 25, 'headloss': 31444, 'velocity': 4.78},
                    {'nominal_diameter': 32, 'headloss': 6889, 'velocity': 2.74},
                    {'nominal_diameter': 40, 'headloss': 3021, 'velocity': 2.02},
                    {'nominal_diameter': 50, 'headloss': 837, 'velocity': 1.26},
                    {'nominal_diameter': 65, 'headloss': 204, 'velocity': 0.75},
                    {'nominal_diameter': 80, 'headloss': 85, 'velocity': 0.54},
                    {'nominal_diameter': 100, 'headloss': 21, 'velocity': 0.32},
                    {'nominal_diameter': 125, 'headloss': 7, 'velocity': 0.21},
                    {'nominal_diameter': 150, 'headloss': 3, 'velocity': 0.15},
                ],
            },
        ),
    ),
)
def test_selecting_optimum_pipe_size(app_fixture, req_json, expected_resp):
    resp = app_fixture.post('/calculate/pipes', json=req_json)
    assert resp.get_json() == expected_resp


@pytest.mark.parametrize(
    'req_json',
    (
        {
            'fluid': 'water',
            'temperature': 20.55,
            'material': 'steel',
            'roughness': 1.5,
            'flow': 10,
            'flow_unit': 'm3/h',
        },
        {
            'fluid': 'water2222',
            'temperature': 20.5,
            'material': 'steel',
            'roughness': 1.5,
            'flow': 10,
            'flow_unit': 'm3/h',
        },
    ),
)
def test_selecting_optimum_pipe_size_failed(app_fixture, req_json):
    resp = app_fixture.post('/calculate/pipes', json=req_json)
    assert resp.get_json() == {'status': 400, 'message': 'Missing or invalid JSON request.'}


def test_not_found(app_fixture):
    resp = app_fixture.post('/not/existing/path')
    assert resp.status_code == 404
    assert resp.get_json() == {'status': 404, 'message': 'not found'}
