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
    ),
)
def test_headloss_endpoint(app_fixture, req_json, expected_resp):
    resp = app_fixture.post('/calculate/headloss', json=req_json)
    assert resp.get_json() == expected_resp
