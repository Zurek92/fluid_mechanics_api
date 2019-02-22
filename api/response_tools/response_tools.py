#!/usr/bin/env python3
from flask import jsonify


def api_response(content):
    """Proper API response as json."""
    response = jsonify(content)
    return response


def error_response(status_code, message):
    """Custom error response.

    :param status_code: response status code
    :param message: error message
    """
    response = jsonify({'status': status_code, 'message': message})
    response.status_code = status_code
    return response
