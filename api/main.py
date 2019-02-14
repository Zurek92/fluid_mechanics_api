#!/usr/bin/env python3
from flask import Flask

from config import API
from endpoints import api

app = Flask(__name__)

app.register_blueprint(api)

if __name__ == '__main__':
    app.run(host=API.IP, port=API.PORT, debug=True)
