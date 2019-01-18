#!/usr/bin/env python3
from flask import Flask

from endpoints import api_endpoints

app = Flask(__name__)

app.register_blueprint(api_endpoints)

if __name__ == '__main__':
    app.run()
