from flask import Blueprint
from flask_restplus import Api

from app.main.controllers.package_controller import api as package_ns

blueprint = Blueprint("api", __name__)

api = Api(
    blueprint,
    title="R CRAN Indexer",
    version="1.0",
    description="API to list packages registered on CRAN for R",
)

api.add_namespace(package_ns, path="/packages")
