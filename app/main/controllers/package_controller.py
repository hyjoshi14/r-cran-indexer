from flask_restplus import Resource, reqparse

from app.main.services import get_packages
from app.main.util import Package

api = Package.api
package = Package.model

parser = reqparse.RequestParser()
parser.add_argument("search", type=str, help="Packages to search for")


@api.route("/", methods=["GET"])
class PackageList(Resource):
    @api.doc("List of Packages")
    @api.expect(parser)
    @api.marshal_list_with(package, envelope="data")
    def get(self):
        args = parser.parse_args()
        query_string = args["search"]
        return get_packages(query_string)
