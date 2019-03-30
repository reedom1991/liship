# -*- coding: utf-8 -*-

from flask import Blueprint


liship = Blueprint('liship', __name__, url_prefix='/liship')

from liship.api import lishipview