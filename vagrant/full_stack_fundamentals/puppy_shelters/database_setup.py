from sqlalchemy import create_engine
from puppyapp.models import Base


engine = create_engine("sqlite:///puppies.db")
Base.metadata.create_all(engine)
