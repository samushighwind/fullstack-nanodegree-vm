from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Shelter, Puppy, PuppyProfile, Adopter
from flask import Flask, request, redirect, render_template, url_for, flash
import datetime
import random


app = Flask(__name__)

engine = create_engine("sqlite:///puppies.db")
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


#All CRUD operations on Puppies, Shelters, and Owners
#Switching or Balancing Shelter Population and Protecting against overflows
#Viewing a Puppy Profile
#Adopting a New Puppy
#Creating and Styling Templates (optionally with Bootstrap)
#Adding Flash Messages
#BONUS: Pagination


# filter to map lists of Puppy, Shelter, or
# Adopter objects to lists of names
@app.template_filter('names')
def names_filter(obj_list):
    return [o.name for o in obj_list]


@app.template_filter('one_dec_place')
def one_dec_place_filter(f):
    return round(float(f) / 0.1) * 0.1


#PUPPY SPECIFIC OPERATIONS

@app.route("/")
@app.route("/puppies/")
def puppy_list():
    puppies = session.query(Puppy).all()
    return render_template("puppy_list.html", puppies=puppies)


@app.route("/puppies/<int:puppy_id>/")
def puppy(puppy_id):
    puppy = session.query(Puppy).filter_by(id=puppy_id).one()
    return render_template("puppy.html", puppy=puppy)


@app.route("/puppies/new/", methods=["GET", "POST"])
def new_puppy():
    if request.method == "POST":
        f = request.form
        new_puppy = Puppy(
            name=f["name"],
            gender=f["gender"],
            date_of_birth=datetime.date(*map(
                lambda d: int(d),
                f["birthdate"].split("-")
            )),
            weight_lbs=float(f["weight"]),
            profile=PuppyProfile(
                picture=f["picture"],
                description=f["description"],
                special_needs=f["special_needs"]
            )
        )
        session.add_all([new_puppy, new_puppy.profile])
        session.commit()
        return redirect(url_for("puppy", puppy_id=new_puppy.id))

    return render_template("new_puppy.html")


@app.route("/puppies/<int:puppy_id>/edit/", methods=["GET", "POST"])
def edit_puppy(puppy_id):
    if request.method == "POST":
        f = request.form
        puppy = session.query(Puppy).filter_by(id=puppy_id).one()
        puppy.name = f["name"]
        puppy.gender = f["gender"]
        puppy.date_of_birth = datetime.date(*map(
            lambda d: int(d),
            f["birthdate"].split("-")
        ))
        puppy.weight_lbs = float(f["weight"])
        puppy.profile.picture = f["picture"]
        puppy.profile.description = f["description"]
        puppy.special_needs = f["special_needs"]
        session.add_all([puppy, puppy.profile])
        session.commit()
        return redirect(url_for("puppy", puppy_id=puppy_id))

    puppy = session.query(Puppy).filter_by(id=puppy_id).one()
    return render_template("edit_puppy.html", puppy=puppy)


@app.route("/puppies/<int:puppy_id>/delete/", methods=["GET", "POST"])
def delete_puppy(puppy_id):
    if request.method == "POST":
        puppy = session.query(Puppy).filter_by(id=puppy_id).one()
        session.delete(puppy)
        session.commit()
        return redirect(url_for("puppy_list"))

    puppy = session.query(Puppy).filter_by(id=puppy_id).one()
    return render_template("delete_puppy.html", puppy=puppy)


def transfer_puppy(puppy, new_shelter, old_shelter=None):
    puppy.shelter_id = new_shelter.id
    new_shelter.current_occupancy += 1
    session.add_all([puppy, new_shelter])
    if old_shelter:
        old_shelter.current_occupancy -= 1
        session.add(old_shelter)
    if len(puppy.adopters):
        del puppy.adopters[:]
    session.commit()


def check_in_puppy(puppy, shelter=None):
    """
    Checks puppy into open shelter (the supplied one, if given and open).

    Args:
      puppy: the Puppy instance to check into the shelter
      shelter: the Shelter where we intend to house the Puppy

    Returns:
      A status message indicating the shelter where the puppy was
      checked in. If all shelters were full, the message will
      indicate that the puppy was not successfully checked in.
    """
    if shelter and puppy.shelter_id and puppy.shelter_id == shelter.id:
        return puppy.name + " was already checked into " + shelter.name + "."

    open_shelters = session.query(Shelter).filter(
        Shelter.current_occupancy < Shelter.maximum_capacity
    ).all()

    if len(open_shelters) == 0:
        return "No shelter has room to take in " + puppy.name + "!"

    if shelter and shelter in open_shelters:
        transfer_puppy(puppy, shelter, puppy.shelter)
        return puppy.name + " was checked into " + shelter.name + "."
    
    # a shelter is randomly chosen from among all shelters sharing
    # the lowest occupancy count, so as to balance capacity but also avoid
    # distribution bias
    minimum_occupancy = min([s.current_occupancy for s in open_shelters])
    new_shelter = random.choice(filter(
        lambda s: s.current_occupancy == minimum_occupancy,
        open_shelters
    ))
    transfer_puppy(puppy, new_shelter, puppy.shelter)

    if shelter:
        return shelter.name + " was beyond capacity, so " + puppy.name + \
            " was checked into " + new_shelter.name + "."

    return puppy.name + " was checked into " + new_shelter.name + "."


@app.route("/puppies/<int:puppy_id>/switch_shelter/", methods=["GET", "POST"])
def switch_shelter(puppy_id):
    if request.method == "POST":
        puppy = session.query(Puppy).filter_by(id=puppy_id).one()
        shelter_id = request.form["shelter_id"]
        shelter = session.query(Shelter).filter_by(id=shelter_id).one()
        flash(check_in_puppy(puppy, shelter))
        return redirect(url_for("puppy", puppy_id=puppy_id))

    puppy = session.query(Puppy).filter_by(id=puppy_id).one()
    shelters = session.query(Shelter).all()
    return render_template(
        "switch_shelter.html",
        puppy=puppy,
        shelters=shelters
    )


def process_puppy_adoption(puppy_id, adopter_ids):
    """
    Has puppy with given id adopted by adopters with given ids.
    Also removes exisiting relationships.

    Args:
      puppy_id: the id of the puppy to be adopted
      adopter_ids: a list of ids belonging to adopters

    Returns:
      A status message indicating who adopted the puppy.
    """
    puppy = session.query(Puppy).filter_by(id=puppy_id).one()
    adopters = session.query(Adopter).filter(Adopter.id.in_(adopter_ids)).all()
    old_adopters = puppy.adopters
    old_shelter = puppy.shelter
    puppy.shelter = None
    del puppy.adopters[:]
    if old_shelter:
        old_shelter.current_occupancy -= 1
        session.add(old_shelter)
    puppy.adopters.extend(adopters)
    session.add(puppy)
    session.commit()
    adopter_names = [a.name for a in adopters]
    return puppy.name + " was adopted by " + ", ".join(adopter_names)


@app.route("/puppies/<int:puppy_id>/adopt/", methods=["GET", "POST"])
def adopt_puppy(puppy_id):
    if request.method == "POST":
        adopter_ids = [int(id) for id in request.form.getlist("adopter_id")]
        flash(process_puppy_adoption(puppy_id, adopter_ids))
        return redirect(url_for("puppy", puppy_id=puppy_id))

    puppy = session.query(Puppy).filter_by(id=puppy_id).one()
    adopters = session.query(Adopter).all()
    return render_template("adopt_puppy.html", puppy=puppy, adopters=adopters)


#ADOPTER SPECIFIC OPERATIONS

@app.route("/adopters/")
def adopter_list():
    adopters = session.query(Adopter).all()
    return render_template("adopter_list.html", adopters=adopters)


@app.route("/adopters/<int:adopter_id>/")
def adopter(adopter_id):
    adopter = session.query(Adopter).filter_by(id=adopter_id).one()
    return render_template("adopter.html", adopter=adopter)


@app.route("/adopters/new/", methods=["GET", "POST"])
def new_adopter():
    if request.method == "POST":
        new_adopter = Adopter(name=request.form["name"])
        session.add(new_adopter)
        session.commit()
        return redirect(url_for("adopter", adopter_id=new_adopter.id))

    return render_template("new_adopter.html")


@app.route("/adopters/<int:adopter_id>/edit/", methods=["GET", "POST"])
def edit_adopter(adopter_id):
    if request.method == "POST":
        adopter = session.query(Adopter).filter_by(id=adopter_id).one()
        adopter.name = request.form["name"]
        session.add(adopter)
        session.commit()
        return redirect(url_for("adopter", adopter_id=adopter_id))

    adopter = session.query(Adopter).filter_by(id=adopter_id).one()
    return render_template("edit_adopter.html", adopter=adopter)


@app.route("/adopters/<int:adopter_id>/delete/", methods=["GET", "POST"])
def delete_adopter(adopter_id):
    if request.method == "POST":
        adopter = session.query(Adopter).filter_by(id=adopter_id).one()
        session.delete(adopter)
        session.commit()
        return redirect(url_for("adopter_list"))

    adopter = session.query(Adopter).filter_by(id=adopter_id).one()
    return render_template("delete_adopter.html", adopter=adopter)


#SHELTER SPECIFIC OPERATIONS

@app.route("/shelters/")
def shelter_list():
    shelters = session.query(Shelter).all()
    return render_template("shelter_list.html", shelters=shelters)


@app.route("/shelters/<int:shelter_id>/")
def shelter(shelter_id):
    shelter = session.query(Shelter).filter_by(id=shelter_id).one()
    return render_template("shelter.html", shelter=shelter)


@app.route("/shelters/new/", methods=["GET", "POST"])
def new_shelter():
    if request.method == "POST":
        f = request.form
        new_shelter = Shelter(
            name=f["name"],
            address=f["address"],
            city=f["city"],
            state=f["state"],
            zip_code=f["zip_code"],
            website=f["website"],
            maximum_capacity=f["maximum_capacity"]
        )
        session.add(new_shelter)
        session.commit()
        return redirect(url_for("shelter", shelter_id=new_shelter.id))

    return render_template("new_shelter.html")


@app.route("/shelters/<int:shelter_id>/edit/", methods=["GET", "POST"])
def edit_shelter(shelter_id):
    if request.method == "POST":
        f = request.form
        shelter = session.query(Shelter).filter_by(id=shelter_id).one()
        shelter.name=f["name"]
        shelter.address=f["address"]
        shelter.city=f["city"]
        shelter.state=f["state"]
        shelter.zip_code=f["zip_code"]
        shelter.website=f["website"]
        shelter.maximum_capacity=f["maximum_capacity"]
        session.add(shelter)
        session.commit()
        return redirect(url_for("shelter", shelter_id=shelter_id))

    shelter = session.query(Shelter).filter_by(id=shelter_id).one()
    return render_template("edit_shelter.html", shelter=shelter)


@app.route("/shelters/<int:shelter_id>/delete/", methods=["GET", "POST"])
def delete_shelter(shelter_id):
    if request.method == "POST":
        shelter = session.query(Shelter).filter_by(id=shelter_id).one()
        session.delete(shelter)
        session.commit()
        return redirect(url_for("shelter_list"))

    shelter = session.query(Shelter).filter_by(id=shelter_id).one()
    return render_template("delete_shelter.html", shelter=shelter)


if __name__ == "__main__":
    app.secret_key = "super_secret_key"
    app.debug = True
    app.run(host="0.0.0.0", port=5000)
