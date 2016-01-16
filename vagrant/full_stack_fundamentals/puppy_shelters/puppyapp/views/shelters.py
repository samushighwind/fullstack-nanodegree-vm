from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask.ext.wtf import Form
from .helpers import get_results_for_current_page
from ..models import Shelter, Puppy
from ..forms import ShelterProfileForm
from ..db import db


shelters_bp = Blueprint("shelters", __name__)


@shelters_bp.route("/")
def list_all():
    (shelters, page, pagelimit) = get_results_for_current_page(
        Shelter.query,
        Shelter.name
    )
    return render_template(
        "shelters/list_all.jinja2",
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
        "shelters/profile.jinja2",
        shelter=shelter,
        puppies=puppies,
        page=page,
        pagelimit=pagelimit
    )


@shelters_bp.route("/new/", methods=["GET", "POST"])
def new():
    form = ShelterProfileForm()

    if form.validate_on_submit():
        new_shelter = Shelter(
            name=form.name.data,
            address=form.address.data,
            city=form.city.data,
            state=form.state.data,
            zip_code=form.zip_code.data,
            website=form.website.data,
            maximum_capacity=form.maximum_capacity.data
        )
        db.session.add(new_shelter)
        db.session.commit()
        flash(new_shelter.name + " has been registered!")
        return redirect(url_for("shelters.profile", shelter_id=new_shelter.id))

    return render_template("shelters/new.jinja2", form=form)


@shelters_bp.route("/<int:shelter_id>/edit/", methods=["GET", "POST"])
def edit(shelter_id):
    shelter = Shelter.query.filter_by(id=shelter_id).one()
    form = ShelterProfileForm()

    if form.is_submitted():
        shelter.name = form.name.data
        shelter.address = form.address.data
        shelter.city = form.city.data
        shelter.state = form.state.data
        shelter.zip_code = form.zip_code.data
        shelter.website = form.website.data
        shelter.maximum_capacity = form.maximum_capacity.data

        if form.validate():
            db.session.add(shelter)
            db.session.commit()
            flash(shelter.name + "'s information has been updated.")
            return redirect(url_for("shelters.profile", shelter_id=shelter_id))

    return render_template("shelters/edit.jinja2", form=form, shelter=shelter)


@shelters_bp.route("/<int:shelter_id>/delete/", methods=["GET", "POST"])
def delete(shelter_id):
    shelter = Shelter.query.filter_by(id=shelter_id).one()
    form = Form()

    if form.validate_on_submit():
        db.session.delete(shelter)
        db.session.commit()
        flash(shelter.name + " was deleted from the database.")
        return redirect(url_for("shelters.list_all"))

    return render_template("shelters/delete.jinja2", form=form, shelter=shelter)
