from app.main.models import Package


def get_packages(query_string):
    packages = Package.query.filter(Package.name.contains(query_string)).all()
    if not packages:
        response_object = []
    else:
        response_object = [
            {
                "name": package.name,
                "version": package.version,
                "title": package.title,
                "description": package.description,
                "published_at": package.published_at,
                "authors": package.authors.split(","),
                "maintainers": package.maintainers.split(","),
                "maintainers_email": package.maintainers_email.split(","),
            }
            for package in packages
        ]
    return response_object, 200
