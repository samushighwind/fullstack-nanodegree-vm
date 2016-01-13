from flask import Flask
from .views.puppies import puppies_bp, home_bp
from .views.adopters import adopters_bp
from .views.shelters import shelters_bp
from .util.filters import names_filter, one_dec_place_filter

app = Flask(__name__)

app.register_blueprint(home_bp)
app.register_blueprint(puppies_bp, url_prefix="/puppies")
app.register_blueprint(adopters_bp, url_prefix="/adopters")
app.register_blueprint(shelters_bp, url_prefix="/shelters")

app.jinja_env.filters["names"] = names_filter
app.jinja_env.filters["one_dec_place"] = one_dec_place_filter
