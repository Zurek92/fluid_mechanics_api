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


def test_not_found(app_fixture):
    resp = app_fixture.post('/not/existing/path')
    assert resp.status_code == 404
    assert resp.get_json() == {'status': 404, 'message': 'not found'}
