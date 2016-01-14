"""
Deletes, recreates and repopulates database in puppyapp directory
"""

from puppyapp import app, db
from puppypopulator import populate
import datetime
import random
import os

try:
    os.remove("./puppyapp/puppies.db")
except OSError:
    pass

with app.app_context():
  db.create_all()
  populate()
