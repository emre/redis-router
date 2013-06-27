# -*- coding: utf8 -*-

try:
    from flask import Flask, render_template, jsonify, request
except ImportError:
    raise ImportError('flask library is not installed.')

from router import Router

import os

# initialize flask application
app = Flask(__name__)

config_file = os.getenv('ROUTER_CONFIG_FILE', '/etc/redis_router/servers.config')

# main view
@app.route('/', methods=['POST', ])
def index():
    router = Router(config_file)
    command, arguments = request.form['command'], request.form['arguments']

    arguments = arguments.split(",")
    router_response = getattr(router, command)(*arguments)
    if isinstance(router_response, set):
        router_response = list(router_response)

    return jsonify({"response": router_response})

from gevent.wsgi import WSGIServer


def start_server(host, port):
    http_server = WSGIServer((host, port), app)
    http_server.serve_forever()
