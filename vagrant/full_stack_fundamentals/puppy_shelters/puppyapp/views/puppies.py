from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import date
from .helpers import get_results_for_current_page
from ..models import Puppy, PuppyProfile, Adopter, Shelter
from ..actions import check_in_puppy, process_puppy_adoption
from ..db import db


puppies_bp = Blueprint("puppies", __name__)


@puppies_bp.route("/")
def list_all():
    (puppies, page, pagelimit) = get_results_for_current_page(
        Puppy.query,
        Puppy.name
    )
    return render_template(
        "puppy_list.html",
        puppies=puppies,
        page=page,
        pagelimit=pagelimit
    )


@puppies_bp.route("/<int:puppy_id>/")
def profile(puppy_id):
    puppy = Puppy.query.filter_by(id=puppy_id).one()
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
        db.session.add_all([new_puppy, new_puppy.profile])
        db.session.commit()
        flash(new_puppy.name + " has been registered!")
        return redirect(url_for("puppies.profile", puppy_id=new_puppy.id))

    return render_template("new_puppy.html")


@puppies_bp.route("/<int:puppy_id>/edit/", methods=["GET", "POST"])
def edit(puppy_id):
    if request.method == "POST":
        f = request.form
        puppy = Puppy.query.filter_by(id=puppy_id).one()
        puppy.name = f["name"]
        puppy.gender = f["gender"]
        puppy.date_of_birth = date(*[int(d) for d in f["birthdate"].split("-")])
        puppy.weight_lbs = float(f["weight"])
        puppy.profile.picture = f["picture"]
        puppy.profile.description = f["description"]
        puppy.special_needs = f["special_needs"]
        db.session.add_all([puppy, puppy.profile])
        db.session.commit()
        flash(puppy.name + "'s information has been updated.")
        return redirect(url_for("puppies.profile", puppy_id=puppy_id))

    puppy = Puppy.query.filter_by(id=puppy_id).one()
    return render_template("edit_puppy.html", puppy=puppy)


@puppies_bp.route("/<int:puppy_id>/delete/", methods=["GET", "POST"])
def delete(puppy_id):
    if request.method == "POST":
        puppy = Puppy.query.filter_by(id=puppy_id).one()
        db.session.delete(puppy)
        db.session.commit()
        flash(puppy.name + " was put to sleep.")
        return redirect(url_for("puppies.list_all"))

    puppy = Puppy.query.filter_by(id=puppy_id).one()
    return render_template("delete_puppy.html", puppy=puppy)


@puppies_bp.route("/<int:puppy_id>/switch_shelter/", methods=["GET", "POST"])
def new_shelter(puppy_id):
    if request.method == "POST":
        puppy = Puppy.query.filter_by(id=puppy_id).one()
        shelter_id = request.form["shelter_id"]
        shelter = Shelter.query.filter_by(id=shelter_id).one()
        flash(check_in_puppy(puppy, shelter))
        return redirect(url_for("puppies.profile", puppy_id=puppy_id))

    puppy = Puppy.query.filter_by(id=puppy_id).one()
    shelters = Shelter.query.order_by(Shelter.name).all()
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

    puppy = Puppy.query.filter_by(id=puppy_id).one()
    adopters = Adopter.query.order_by(Adopter.name).all()
    return render_template("adopt_puppy.html", puppy=puppy, adopters=adopters)



home_bp = Blueprint("home", __name__)


@home_bp.route("/")
def home():
    return list_all()
