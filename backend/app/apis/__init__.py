from flask import Blueprint
from flask_restx import Api
# from .test_api import test as ns
from .course import api as ns1

blueprint = Blueprint('api', __name__)

api = Api(
    blueprint,
    title="API",
    version="1.0",
    doc="/docs"
)

# Api factory
# api.add_namespace(ns, path="/test")
api.add_namespace(ns1, path='/course')