import logging.config
import json

import yaml
from flask import Flask, request, jsonify

logging.config.dictConfig(yaml.load(open('logging.yaml')))
r_logger = logging.getLogger('rlogger')

app = Flask(__name__)


@app.route('/', methods=["POST", "GET"])
def hello_world():
    message = "IP : {}, Data : {}, Form : {}".format(request.remote_addr, request.data, json.dumps(request.form))
    r_logger.info(message)
    return message


@app.route('/logs/rlogger', methods=["GET", ])
def logs_wsgi():
    with open("logs/rlogger.log") as f:
        message = f.read()
        return message


@app.route('/logs/error', methods=["GET", ])
def logs_error():
    with open("logs/errors.log") as f:
        message = f.read()
        return message
