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
    assert resp.headers.get('Access-Control-Allow-Origin') == 'http://localhost:13000'
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
        (
            {
                'fluid': 'water',
                'temperature_supply': 90,
                'temperature_return': 70,
                'nominal_diameter': 50,
                'material': 'steel',
                'power': 81534.02,
                'power_unit': 'W',
                'length': 10,
                'headloss_unit': 'kPa',
            },
            {'headloss': 1.04, 'headloss_unit': 'kPa', 'velocity': 0.45, 'velocity_unit': 'm/s'},
        ),
        (
            {
                'fluid': 'water',
                'temperature_supply': 90,
                'temperature_return': 70,
                'nominal_diameter': 50,
                'material': 'steel',
                'power': 81.53402,
                'power_unit': 'kW',
                'length': 10,
                'headloss_unit': 'kPa',
            },
            {'headloss': 1.04, 'headloss_unit': 'kPa', 'velocity': 0.45, 'velocity_unit': 'm/s'},
        ),
        (
            {
                'fluid': 'water',
                'temperature': 30,
                'nominal_diameter': 25,
                'material': 'steel',
                'flow': 0,
                'flow_unit': 'm3/h',
                'length': 10,
            },
            {'velocity': 0, 'velocity_unit': 'm/s', 'headloss': 0, 'headloss_unit': 'Pa'},
        ),
    ),
)
def test_headloss_endpoint(app_fixture, req_json, expected_resp):
    resp = app_fixture.post('/calculate/headloss', json=req_json)
    assert resp.get_json() == expected_resp


@pytest.mark.parametrize(
    'req_json',
    (
        None,
        {
            'fluid': 'water',
            'temperature': 30,
            'nominal_diameter': 25,
            'material': 'steel',
            'flow': 10,
            'flow_unit': 'm3/h',
            'length': -1,
        },
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
        {
            'fluid': 'water',
            'temperature': 30,
            'nominal_diameter': 24,
            'material': 'steel',
            'flow': 10,
            'flow_unit': 'm3/h',
            'length': 1,
        },
    ),
)
def test_headloss_endpoint_failed(app_fixture, req_json):
    resp = app_fixture.post('/calculate/headloss', json=req_json)
    assert resp.status_code == 400


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
        (
            {
                'fluid': 'water',
                'temperature_supply': 80,
                'temperature_return': 50,
                'material': 'steel',
                'roughness': 1,
                'power': 50,
                'power_unit': 'kW',
            },
            {
                'headloss_unit': 'Pa/m',
                'velocity_unit': 'm/s',
                'results': [
                    {'headloss': 270966.0, 'nominal_diameter': 8, 'velocity': 6.68},
                    {'headloss': 38673.0, 'nominal_diameter': 10, 'velocity': 3.31},
                    {'headloss': 9877.0, 'nominal_diameter': 15, 'velocity': 2.02},
                    {'headloss': 1930.0, 'nominal_diameter': 20, 'velocity': 1.11},
                    {'headloss': 548.0, 'nominal_diameter': 25, 'velocity': 0.7},
                    {'headloss': 120.0, 'nominal_diameter': 32, 'velocity': 0.4},
                    {'headloss': 55.0, 'nominal_diameter': 40, 'velocity': 0.3},
                    {'headloss': 14.0, 'nominal_diameter': 50, 'velocity': 0.18},
                    {'headloss': 4.0, 'nominal_diameter': 65, 'velocity': 0.11},
                    {'headloss': 2.0, 'nominal_diameter': 80, 'velocity': 0.08},
                    {'headloss': 0.0, 'nominal_diameter': 100, 'velocity': 0.05},
                    {'headloss': 0.0, 'nominal_diameter': 125, 'velocity': 0.03},
                    {'headloss': 0.0, 'nominal_diameter': 150, 'velocity': 0.02},
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
    assert resp.status_code == 400


@pytest.mark.parametrize(
    'req_json, expected_resp',
    (
        (
            {'width': 1, 'height': 1, 'slope': 0.01, 'manning_coefficient': 0.013},
            {'velocity': 3.7, 'velocity_unit': 'm/s', 'flow': 13313.07, 'flow_unit': 'm3/h'},
        ),
        (
            {'diameter': 0.1, 'height': 0.1, 'slope': 0.05, 'manning_coefficient': 0.013},
            {'velocity': 1.47, 'velocity_unit': 'm/s', 'flow': 41.58, 'flow_unit': 'm3/h'},
        ),
    ),
)
def test_gravity_flow(app_fixture, req_json, expected_resp):
    resp = app_fixture.post('/calculate/gravity_flow', json=req_json)
    assert resp.get_json() == expected_resp


@pytest.mark.parametrize(
    'req_json',
    (
        # both width and height
        {'width': 1, 'diameter': 0.1, 'height': 1, 'slope': 0.01, 'manning_coefficient': 0.013},
        # height > diameter
        {'diameter': 0.1, 'height': 1, 'slope': 0.01, 'manning_coefficient': 0.013},
    ),
)
def test_gravity_flow_failed(app_fixture, req_json):
    resp = app_fixture.post('/calculate/gravity_flow', json=req_json)
    assert resp.status_code == 400


def test_not_found(app_fixture):
    resp = app_fixture.post('/not/existing/path')
    assert resp.status_code == 404


@pytest.mark.parametrize('path', ('/calculate/headloss', '/calculate/pipes', '/calculate/gravity_flow'))
def test_wrong_method(app_fixture, path):
    resp = app_fixture.get(path)
    assert resp.status_code == 405
