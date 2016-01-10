from sqlalchemy import Table, Column, ForeignKey, Integer, String, Date, Numeric
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref, mapper
from sqlalchemy import create_engine, event
from sqlalchemy.inspection import inspect

Base = declarative_base()

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


class Shelter(Base):
    __tablename__ = "shelter"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    address = Column(String(250))
    city = Column(String(80))
    state = Column(String(20))
    zip_code = Column(String(10))
    website = Column(String)
    maximum_capacity = Column(Integer, nullable=False)
    current_occupancy = Column(Integer, default=0, nullable=False)

    # establishes One-to-Many relationship between Shelter and Puppy
    puppies = relationship("Puppy", backref="shelter")


class Puppy(Base):
    __tablename__ = "puppy"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    gender = Column(String(6), nullable=False)
    date_of_birth = Column(Date, nullable=False)
    weight_lbs = Column(Numeric(10), nullable=False)
    shelter_id = Column(Integer, ForeignKey("shelter.id"), nullable=False)
    profile_id = Column(Integer, ForeignKey("puppy_profile.id"))
    
    # establishes One-to-One relationship between Puppy and PuppyProfile
    # (without `useList=False`, could be Many-to-One)
    profile = relationship(
        "PuppyProfile",
        cascade="all, delete-orphan",
        backref=backref("puppy", uselist=False)
    )


class PuppyProfile(Base):
    __tablename__ = "puppy_profile"

    id = Column(Integer, primary_key=True)
    picture = Column(String)
    description = Column(String)
    special_needs = Column(String)


class Adopter(Base):
    __tablename__ = "adopter"

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)

    # establishes Many-to-Many relationship between Adopter and Puppy
    puppies = relationship(
        "Puppy",
        # evaluated later, so table can be defined below
        secondary=lambda: puppy_adopter_association,
        backref="adopters"
    )


# association table between Puppy and Adopter
puppy_adopter_association = Table("puppy_adopter_association", Base.metadata,
    Column("puppy_id", Integer, ForeignKey("puppy.id")),
    Column("adopter_id", Integer, ForeignKey("adopter.id"))
)


engine = create_engine("sqlite:///puppies.db")
Base.metadata.create_all(engine)
