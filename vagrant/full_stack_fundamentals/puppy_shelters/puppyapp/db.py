from sqlalchemy import event
from sqlalchemy.orm import mapper
from sqlalchemy.inspection import inspect
from flask.ext.sqlalchemy import SQLAlchemy


# fill in defaults on init so they will be available prior to commit
# (event handler found at http://stackoverflow.com/a/24893168/4956731)
@event.listens_for(mapper, "init")
def fill_defaults_on_init(target, args, kwargs):
    for key, column in inspect(target.__class__).columns.items():
        if column.default is not None:
            if callable(column.default.arg):
                setattr(target, key, column.default.arg(target))
            else:
                setattr(target, key, column.default.arg)


db = SQLAlchemy()
