from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask.ext.wtf import Form
from .helpers import get_results_for_current_page
from ..models import Adopter, Puppy
from ..forms import AdopterProfileForm
from ..db import db


adopters_bp = Blueprint("adopters", __name__)


@adopters_bp.route("/")
def list_all():
    (adopters, page, pagelimit) = get_results_for_current_page(
        Adopter.query,
        Adopter.name
    )
    return render_template(
        "adopters/list_all.html",
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
        "adopters/profile.html",
        adopter=adopter,
        puppies=puppies,
        page=page,
        pagelimit=pagelimit
    )


@adopters_bp.route("/new/", methods=["GET", "POST"])
def new():
    form = AdopterProfileForm()

    if form.validate_on_submit():
        new_adopter = Adopter(name=form.name.data)
        db.session.add(new_adopter)
        db.session.commit()
        flash(new_adopter.name + " has been registered!")
        return redirect(url_for("adopters.profile", adopter_id=new_adopter.id))

    return render_template("adopters/new.html", form=form)


@adopters_bp.route("/<int:adopter_id>/edit/", methods=["GET", "POST"])
def edit(adopter_id):
    adopter = Adopter.query.filter_by(id=adopter_id).one()
    form = AdopterProfileForm()

    if form.is_submitted():
        adopter.name = form.name.data

        if form.validate():
            db.session.add(adopter)
            db.session.commit()
            flash(adopter.name + "'s information has been updated.")
            return redirect(url_for("adopters.profile", adopter_id=adopter_id))

    return render_template("adopters/edit.html", form=form, adopter=adopter)


@adopters_bp.route("/<int:adopter_id>/delete/", methods=["GET", "POST"])
def delete(adopter_id):
    adopter = Adopter.query.filter_by(id=adopter_id).one()
    # we can use a generic form, since there are no fields
    form = Form()

    if form.validate_on_submit():
        db.session.delete(adopter)
        db.session.commit()
        flash(adopter.name + " was deleted from the database.")
        return redirect(url_for("adopters.list_all"))

    return render_template("adopters/delete.html", form=form, adopter=adopter)