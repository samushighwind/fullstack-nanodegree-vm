from flask import Blueprint, render_template, request, redirect, url_for, flash
from .helpers import get_results_for_current_page
from ..models import Adopter, Puppy
from ..db import db


adopters_bp = Blueprint("adopters", __name__)


@adopters_bp.route("/")
def list_all():
    (adopters, page, pagelimit) = get_results_for_current_page(
        Adopter.query,
        Adopter.name
    )
    return render_template(
        "adopter_list.html",
        adopters=adopters,
        page=page,
        pagelimit=pagelimit
    )


@adopters_bp.route("/<int:adopter_id>/")
def profile(adopter_id):
    adopter = Adopter.query.filter_by(id=adopter_id).one()
    (puppies, page, pagelimit) = get_results_for_current_page(
        adopter.puppies,
        Puppy.name
    )
    return render_template(
        "adopter.html",
        adopter=adopter,
        puppies=puppies,
        page=page,
        pagelimit=pagelimit
    )


@adopters_bp.route("/new/", methods=["GET", "POST"])
def new():
    if request.method == "POST":
        new_adopter = Adopter(name=request.form["name"])
        db.session.add(new_adopter)
        db.session.commit()
        flash(new_adopter.name + " has been registered!")
        return redirect(url_for("adopters.profile", adopter_id=new_adopter.id))

    return render_template("new_adopter.html")


@adopters_bp.route("/<int:adopter_id>/edit/", methods=["GET", "POST"])
def edit(adopter_id):
    if request.method == "POST":
        adopter = Adopter.query.filter_by(id=adopter_id).one()
        adopter.name = request.form["name"]
        db.session.add(adopter)
        db.session.commit()
        flash(adopter.name + "'s information has been updated.")
        return redirect(url_for("adopters.profile", adopter_id=adopter_id))

    adopter = Adopter.query.filter_by(id=adopter_id).one()
    return render_template("edit_adopter.html", adopter=adopter)


@adopters_bp.route("/<int:adopter_id>/delete/", methods=["GET", "POST"])
def delete(adopter_id):
    if request.method == "POST":
        adopter = Adopter.query.filter_by(id=adopter_id).one()
        db.session.delete(adopter)
        db.session.commit()
        flash(adopter.name + " was deleted from the database.")
        return redirect(url_for("adopters.list_all"))

    adopter = Adopter.query.filter_by(id=adopter_id).one()
    return render_template("delete_adopter.html", adopter=adopter)