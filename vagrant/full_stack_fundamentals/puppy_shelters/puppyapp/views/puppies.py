from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import date
from .helpers import get_number_of_pages, get_current_page, ITEMS_PER_PAGE
from ..models import Puppy, PuppyProfile, Adopter, Shelter
from ..actions import check_in_puppy, process_puppy_adoption
from ..db import session


puppies_bp = Blueprint("puppies", __name__)


@puppies_bp.route("/")
def list_all():
    pagelimit = get_number_of_pages(Puppy)
    page = get_current_page(pagelimit)
    puppies = session.query(Puppy) \
                     .offset((page-1) * ITEMS_PER_PAGE) \
                     .limit(ITEMS_PER_PAGE)
    return render_template(
        "puppy_list.html",
        puppies=puppies,
        page=page,
        pagelimit=pagelimit
    )


@puppies_bp.route("/<int:puppy_id>/")
def profile(puppy_id):
    puppy = session.query(Puppy).filter_by(id=puppy_id).one()
    return render_template("puppy.html", puppy=puppy)


@puppies_bp.route("/new/", methods=["GET", "POST"])
def new():
    if request.method == "POST":
        f = request.form
        new_puppy = Puppy(
            name=f["name"],
            gender=f["gender"],
            date_of_birth=date(*[int(d) for d in f["birthdate"].split("-")]),
            weight_lbs=float(f["weight"]),
            profile=PuppyProfile(
                picture=f["picture"],
                description=f["description"],
                special_needs=f["special_needs"]
            )
        )
        session.add_all([new_puppy, new_puppy.profile])
        session.commit()
        flash(new_puppy.name + " has been registered!")
        return redirect(url_for("puppies.profile", puppy_id=new_puppy.id))

    return render_template("new_puppy.html")


@puppies_bp.route("/<int:puppy_id>/edit/", methods=["GET", "POST"])
def edit(puppy_id):
    if request.method == "POST":
        f = request.form
        puppy = session.query(Puppy).filter_by(id=puppy_id).one()
        puppy.name = f["name"]
        puppy.gender = f["gender"]
        puppy.date_of_birth = date(*[int(d) for d in f["birthdate"].split("-")])
        puppy.weight_lbs = float(f["weight"])
        puppy.profile.picture = f["picture"]
        puppy.profile.description = f["description"]
        puppy.special_needs = f["special_needs"]
        session.add_all([puppy, puppy.profile])
        session.commit()
        flash(puppy.name + "'s information has been updated.")
        return redirect(url_for("puppies.profile", puppy_id=puppy_id))

    puppy = session.query(Puppy).filter_by(id=puppy_id).one()
    return render_template("edit_puppy.html", puppy=puppy)


@puppies_bp.route("/<int:puppy_id>/delete/", methods=["GET", "POST"])
def delete(puppy_id):
    if request.method == "POST":
        puppy = session.query(Puppy).filter_by(id=puppy_id).one()
        session.delete(puppy)
        session.commit()
        flash(puppy.name + " was put to sleep.")
        return redirect(url_for("puppies.list_all"))

    puppy = session.query(Puppy).filter_by(id=puppy_id).one()
    return render_template("delete_puppy.html", puppy=puppy)


@puppies_bp.route("/<int:puppy_id>/switch_shelter/", methods=["GET", "POST"])
def new_shelter(puppy_id):
    if request.method == "POST":
        puppy = session.query(Puppy).filter_by(id=puppy_id).one()
        shelter_id = request.form["shelter_id"]
        shelter = session.query(Shelter).filter_by(id=shelter_id).one()
        flash(check_in_puppy(puppy, shelter))
        return redirect(url_for("puppies.profile", puppy_id=puppy_id))

    puppy = session.query(Puppy).filter_by(id=puppy_id).one()
    shelters = session.query(Shelter).all()
    return render_template(
        "switch_shelter.html",
        puppy=puppy,
        shelters=shelters
    )


@puppies_bp.route("/<int:puppy_id>/adopt/", methods=["GET", "POST"])
def adopt(puppy_id):
    if request.method == "POST":
        adopter_ids = [int(id) for id in request.form.getlist("adopter_id")]
        flash(process_puppy_adoption(puppy_id, adopter_ids))
        return redirect(url_for("puppies.profile", puppy_id=puppy_id))

    puppy = session.query(Puppy).filter_by(id=puppy_id).one()
    adopters = session.query(Adopter).all()
    return render_template("adopt_puppy.html", puppy=puppy, adopters=adopters)



home_bp = Blueprint("home", __name__)


@home_bp.route("/")
def home():
    return list_all()
