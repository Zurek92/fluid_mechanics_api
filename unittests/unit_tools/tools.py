#!/usr/bin/env python3
import json


def json_response(response):
    return json.loads(response.get_data().decode())
