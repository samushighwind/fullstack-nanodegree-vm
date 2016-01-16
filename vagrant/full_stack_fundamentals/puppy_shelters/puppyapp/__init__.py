from flask import Flask
from .views.puppies import puppies_bp, home_bp
from .views.adopters import adopters_bp
from .views.shelters import shelters_bp
from .util.filters import filters
from .util.jinja_globals import global_fns
from .db import db

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///puppies.db"
db.init_app(app)

app.register_blueprint(home_bp)
app.register_blueprint(puppies_bp, url_prefix="/puppies")
app.register_blueprint(adopters_bp, url_prefix="/adopters")
app.register_blueprint(shelters_bp, url_prefix="/shelters")

for f in filters:
    app.jinja_env.filters[f.__name__] = f

for g in global_fns:
    app.jinja_env.globals[g.__name__] = g
