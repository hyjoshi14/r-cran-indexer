from app.main import db


class Package(db.Model):

    __tablename__ = "package"
    name = db.Column(db.String(50), nullable=False, primary_key=True)
    version = db.Column(db.String(5), nullable=False, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.Text, nullable=False)
    published_at = db.Column(db.String(15), nullable=False)
    authors = db.Column(db.String(512), nullable=False)
    maintainers = db.Column(db.String(512), nullable=False)
    maintainers_email = db.Column(db.String(512), nullable=False)

    def __init__(
        self,
        name,
        version,
        title,
        description,
        published_at,
        authors,
        maintainers,
        maintainers_email,
    ):
        self.name = name
        self.version = version
        self.title = title
        self.description = description
        self.published_at = published_at
        self.authors = authors
        self.maintainers = maintainers
        self.maintainers_email = maintainers_email

    def __repr__(self):
        return f"<{self.name} - {self.version}>"
