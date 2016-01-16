from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask.ext.wtf import Form
from .helpers import get_results_for_current_page
from ..models import Puppy, PuppyProfile, Adopter, Shelter
from ..actions import check_in_puppy, process_puppy_adoption
from ..forms import PuppyProfileForm, ShelterTransferForm, PuppyAdoptionForm
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
    form = PuppyProfileForm()

    if form.validate_on_submit():
        new_puppy = Puppy(
            name=form.name.data,
            gender=form.gender.data,
            date_of_birth=form.birthdate.data,
            weight_lbs=form.weight.data,
            profile=PuppyProfile(
                picture=form.picture.data,
                description=form.description.data,
                special_needs=form.special_needs.data
            )
        )
        db.session.add_all([new_puppy, new_puppy.profile])
        db.session.commit()
        flash(new_puppy.name + " has been registered!")
        return redirect(url_for("puppies.profile", puppy_id=new_puppy.id))

    return render_template("new_puppy.html", form=form)


@puppies_bp.route("/<int:puppy_id>/edit/", methods=["GET", "POST"])
def edit(puppy_id):
    puppy = Puppy.query.filter_by(id=puppy_id).one()
    form = PuppyProfileForm()

    if form.is_submitted():
        puppy.name = form.name.data
        puppy.gender = form.gender.data
        puppy.date_of_birth = form.birthdate.data
        puppy.weight_lbs = form.weight.data
        puppy.profile.picture = form.picture.data
        puppy.profile.description = form.description.data
        puppy.special_needs = form.special_needs.data

        if form.validate():
            db.session.add_all([puppy, puppy.profile])
            db.session.commit()
            flash(puppy.name + "'s information has been updated.")
            return redirect(url_for("puppies.profile", puppy_id=puppy_id))

    return render_template("edit_puppy.html", form=form, puppy=puppy)


@puppies_bp.route("/<int:puppy_id>/delete/", methods=["GET", "POST"])
def delete(puppy_id):
    puppy = Puppy.query.filter_by(id=puppy_id).one()
    # we can use a generic form, since there are no fields
    form = Form()

    if form.validate_on_submit():
        db.session.delete(puppy)
        db.session.commit()
        flash(puppy.name + " was put to sleep.")
        return redirect(url_for("puppies.list_all"))

    return render_template("delete_puppy.html", form=form, puppy=puppy)


@puppies_bp.route("/<int:puppy_id>/switch_shelter/", methods=["GET", "POST"])
def new_shelter(puppy_id):
    puppy = Puppy.query.filter_by(id=puppy_id).one()
    shelters = Shelter.query.order_by(Shelter.name).all()
    form = ShelterTransferForm()
    choices = [(shelter.id, shelter.name) for shelter in shelters]
    form.shelter_id.choices = choices

    if form.validate_on_submit():
        shelter_id = form.shelter_id.data
        shelter = Shelter.query.filter_by(id=shelter_id).one()
        flash(check_in_puppy(puppy, shelter))
        return redirect(url_for("puppies.profile", puppy_id=puppy_id))

    return render_template(
        "switch_shelter.html",
        form=form,
        puppy=puppy,
        shelters=shelters
    )


@puppies_bp.route("/<int:puppy_id>/adopt/", methods=["GET", "POST"])
def adopt(puppy_id):
    puppy = Puppy.query.filter_by(id=puppy_id).one()
    adopters = Adopter.query.order_by(Adopter.name).all()
    form = PuppyAdoptionForm()
    choices = [(adopter.id, adopter.name) for adopter in adopters]
    form.adopter_ids.choices = choices
    
    if form.validate_on_submit():
        adopter_ids = form.adopter_ids.data
        flash(process_puppy_adoption(puppy_id, adopter_ids))
        return redirect(url_for("puppies.profile", puppy_id=puppy_id))

    return render_template(
        "adopt_puppy.html",
        form=form,
        puppy=puppy,
        adopters=adopters
    )



home_bp = Blueprint("home", __name__)


@home_bp.route("/")
def home():
    return list_all()
