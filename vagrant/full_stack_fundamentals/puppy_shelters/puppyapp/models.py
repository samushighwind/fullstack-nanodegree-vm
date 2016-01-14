from .db import db


class Shelter(db.Model):
    __tablename__ = "shelter"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    address = db.Column(db.String(250))
    city = db.Column(db.String(80))
    state = db.Column(db.String(20))
    zip_code = db.Column(db.String(10))
    website = db.Column(db.String)
    maximum_capacity = db.Column(db.Integer, nullable=False)
    current_occupancy = db.Column(db.Integer, default=0, nullable=False)

    # establishes One-to-Many relationship between Shelter and Puppy
    puppies = db.relationship("Puppy", backref="shelter", lazy="dynamic")


class Puppy(db.Model):
    __tablename__ = "puppy"
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    gender = db.Column(db.String(6), nullable=False)
    date_of_birth = db.Column(db.Date, nullable=False)
    weight_lbs = db.Column(db.Numeric(10), nullable=False)
    shelter_id = db.Column(db.Integer, db.ForeignKey("shelter.id"))
    profile_id = db.Column(db.Integer, db.ForeignKey("puppy_profile.id"), nullable=False)
    
    # establishes One-to-One relationship between Puppy and PuppyProfile
    # (without `useList=False`, could be Many-to-One)
    profile = db.relationship(
        "PuppyProfile",
        cascade="all, delete-orphan",
        single_parent=True,
        backref=db.backref("puppy", uselist=False, single_parent=True)
    )


class PuppyProfile(db.Model):
    __tablename__ = "puppy_profile"

    id = db.Column(db.Integer, primary_key=True)
    picture = db.Column(db.String)
    description = db.Column(db.String)
    special_needs = db.Column(db.String)


class Adopter(db.Model):
    __tablename__ = "adopter"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)

    # establishes Many-to-Many relationship between Adopter and Puppy
    puppies = db.relationship(
        "Puppy",
        # evaluated later, so table can be defined below
        secondary=lambda: puppy_adopter_association,
        backref="adopters",
        lazy="dynamic"
    )


# association table between Puppy and Adopter
puppy_adopter_association = db.Table("puppy_adopter_association",
    db.Column("puppy_id", db.Integer, db.ForeignKey("puppy.id")),
    db.Column("adopter_id", db.Integer, db.ForeignKey("adopter.id"))
)
