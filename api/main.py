#!/usr/bin/env python3
from flask import Flask
from flask_cors import CORS

from config import API
from endpoints import api

app = Flask(__name__)
cors = CORS(app, resources={r'*': {'origins': API.CORS_ORIGIN}})

app.register_blueprint(api)

if __name__ == '__main__':
    app.run(host=API.IP, port=API.PORT, debug=True)
