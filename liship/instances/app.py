# -*- coding: utf-8 -*-
import os
import sys
sys.path.append(os.path.abspath(os.path.dirname(__file__)) + "\\..\\..\\")
from flask import Flask
from liship.api import liship
from liship.schedule import scheduler
from liship.setting import config
import logging.config

logging.config.dictConfig(config["LOGGING_CONFIG"])


def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    app.register_blueprint(liship)

    return app


scheduler.start()
app = create_app(config)
app.run(host='0.0.0.0', port=8080)
