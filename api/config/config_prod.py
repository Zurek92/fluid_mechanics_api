#!/usr/bin/env python3
"""Production config."""
import os


class API:
    IP = "0.0.0.0"
    PORT = os.environ.get('API_PORT')
    CORS_HEADER = os.environ.get('CORS_HEADER')
