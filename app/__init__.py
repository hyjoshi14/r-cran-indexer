from flask import Flask

from app.main import db
from app.main.blueprint import blueprint
from app.main.models import Package

app = Flask(__name__)
app.config.from_object("config")
app.register_blueprint(blueprint)
app.app_context().push()

db.init_app(app)
db.create_all()

session = db.sessionmaker(bind=db.engine)()
