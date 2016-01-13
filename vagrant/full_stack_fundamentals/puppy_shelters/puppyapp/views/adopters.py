from flask import Blueprint, render_template, request, redirect, url_for, flash
from .helpers import get_number_of_pages, get_current_page, ITEMS_PER_PAGE
from ..models import Adopter
from ..db import session


adopters_bp = Blueprint("adopters", __name__)


@adopters_bp.route("/")
def list_all():
    pagelimit = get_number_of_pages(Adopter)
    page = get_current_page(pagelimit)
    adopters = session.query(Adopter) \
                      .offset((page-1) * ITEMS_PER_PAGE) \
                      .limit(ITEMS_PER_PAGE)
    return render_template(
        "adopter_list.html",
        adopters=adopters,
        page=page,
        pagelimit=pagelimit
    )


@adopters_bp.route("/<int:adopter_id>/")
def profile(adopter_id):
    adopter = session.query(Adopter).filter_by(id=adopter_id).one()
    return render_template("adopter.html", adopter=adopter)


@adopters_bp.route("/new/", methods=["GET", "POST"])
def new():
    if request.method == "POST":
        new_adopter = Adopter(name=request.form["name"])
        session.add(new_adopter)
        session.commit()
        flash(new_adopter.name + " has been registered!")
        return redirect(url_for("adopters.profile", adopter_id=new_adopter.id))

    return render_template("new_adopter.html")


@adopters_bp.route("/<int:adopter_id>/edit/", methods=["GET", "POST"])
def edit(adopter_id):
    if request.method == "POST":
        adopter = session.query(Adopter).filter_by(id=adopter_id).one()
        adopter.name = request.form["name"]
        session.add(adopter)
        session.commit()
        flash(adopter.name + "'s information has been updated.")
        return redirect(url_for("adopters.profile", adopter_id=adopter_id))

    adopter = session.query(Adopter).filter_by(id=adopter_id).one()
    return render_template("edit_adopter.html", adopter=adopter)


@adopters_bp.route("/<int:adopter_id>/delete/", methods=["GET", "POST"])
def delete(adopter_id):
    if request.method == "POST":
        adopter = session.query(Adopter).filter_by(id=adopter_id).one()
        session.delete(adopter)
        session.commit()
        flash(adopter.name + " was deleted from the database.")
        return redirect(url_for("adopters.list_all"))

    adopter = session.query(Adopter).filter_by(id=adopter_id).one()
    return render_template("delete_adopter.html", adopter=adopter)