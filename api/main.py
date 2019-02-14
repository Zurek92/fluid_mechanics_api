#!/usr/bin/env python3
from flask import Flask

from config import APP
from endpoints import api

app = Flask(__name__)

app.register_blueprint(api)

if __name__ == '__main__':
    app.run(host=APP.IP, port=APP.PORT, debug=True)
