#!/usr/bin/env python3
from flask import jsonify

from config import API


def api_response(content):
    """Proper API response as json with CORS header."""
    response = jsonify(content)
    response.headers['Access-Control-Allow-Origin'] = API.CORS_HEADER
    return response


def error_response(status_code, message):
    """Custom error response.

    :param status_code: response status code
    :param message: error message
    """
    response = jsonify({'status': status_code, 'message': message})
    response.status_code = status_code
    response.headers['Access-Control-Allow-Origin'] = API.CORS_HEADER
    return response
