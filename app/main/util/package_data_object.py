from flask_restplus import Namespace, fields


class Package:
    api = Namespace("Packages", description="R Packages related operations.")
    model = api.model(
        "package",
        {
            "name": fields.String(required=True, description="Package Name"),
            "version": fields.String(required=True, description="Package Version"),
            "title": fields.String(required=True, description="Package Title"),
            "description": fields.String(
                required=True, description="Package description"
            ),
            "published_at": fields.Date(
                required=True, description="Date Package Published At"
            ),
            "authors": fields.List(
                fields.String, required=True, description="List of authors"
            ),
            "maintainers": fields.List(
                fields.String, required=True, description="List of maintainers"
            ),
            "maintainers_email": fields.List(
                fields.String, required=True, description="List of maintainers"
            ),
        },
    )
