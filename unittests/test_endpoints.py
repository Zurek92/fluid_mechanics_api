#!/usr/bin/env python3
import pytest

from main import app
from unit_tools.tools import json_response


@pytest.fixture()
def app_fixture():
    app.config['TESTING'] = True
    client = app.test_client()
    yield client


def test_simple_endpoint(app_fixture):
    resp = app_fixture.get('/health')
    assert resp.status_code == 200
    assert json_response(resp) == {'status': 'everything is ok :)'}
