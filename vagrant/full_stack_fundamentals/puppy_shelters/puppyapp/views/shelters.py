from flask import Blueprint, render_template, request, redirect, url_for, flash
from .helpers import get_results_for_current_page
from ..models import Shelter, Puppy
from ..db import db


shelters_bp = Blueprint("shelters", __name__)


@shelters_bp.route("/")
def list_all():
    (shelters, page, pagelimit) = get_results_for_current_page(
        Shelter.query,
        Shelter.name
    )
    return render_template(
        "shelter_list.html",
        shelters=shelters,
        page=page,
        pagelimit=pagelimit
    )


@shelters_bp.route("/<int:shelter_id>/")
def profile(shelter_id):
    shelter = Shelter.query.filter_by(id=shelter_id).one()
    (puppies, page, pagelimit) = get_results_for_current_page(
        shelter.puppies,
        Puppy.name
    )
    return render_template(
        "shelter.html",
        shelter=shelter,
        puppies=puppies,
        page=page,
        pagelimit=pagelimit
    )


@shelters_bp.route("/new/", methods=["GET", "POST"])
def new():
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
        db.session.add(new_shelter)
        db.session.commit()
        flash(new_shelter.name + " has been registered!")
        return redirect(url_for("shelters.profile", shelter_id=new_shelter.id))

    return render_template("new_shelter.html")


@shelters_bp.route("/<int:shelter_id>/edit/", methods=["GET", "POST"])
def edit(shelter_id):
    if request.method == "POST":
        f = request.form
        shelter = Shelter.query.filter_by(id=shelter_id).one()
        shelter.name=f["name"]
        shelter.address=f["address"]
        shelter.city=f["city"]
        shelter.state=f["state"]
        shelter.zip_code=f["zip_code"]
        shelter.website=f["website"]
        shelter.maximum_capacity=f["maximum_capacity"]
        db.session.add(shelter)
        db.session.commit()
        flash(shelter.name + "'s information has been updated.")
        return redirect(url_for("shelters.profile", shelter_id=shelter_id))

    shelter = Shelter.query.filter_by(id=shelter_id).one()
    return render_template("edit_shelter.html", shelter=shelter)


@shelters_bp.route("/<int:shelter_id>/delete/", methods=["GET", "POST"])
def delete(shelter_id):
    if request.method == "POST":
        shelter = Shelter.query.filter_by(id=shelter_id).one()
        db.session.delete(shelter)
        db.session.commit()
        flash(shelter.name + " was deleted from the database.")
        return redirect(url_for("shelters.list_all"))

    shelter = Shelter.query.filter_by(id=shelter_id).one()
    return render_template("delete_shelter.html", shelter=shelter)
