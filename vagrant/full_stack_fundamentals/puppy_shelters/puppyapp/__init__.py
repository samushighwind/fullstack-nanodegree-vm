from flask import Flask
from .views.puppies import puppies_bp, home_bp
from .views.adopters import adopters_bp
from .views.shelters import shelters_bp

app = Flask(__name__)
app.register_blueprint(home_bp)
app.register_blueprint(puppies_bp, url_prefix="/puppies")
app.register_blueprint(adopters_bp, url_prefix="/adopters")
app.register_blueprint(shelters_bp, url_prefix="/shelters")

# it's import that this happens AFTER the app has been initialized,
# to prevent circular imports.
from .util import filters
