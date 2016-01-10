from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Restaurant, MenuItem
from flask import Flask, request, redirect, render_template, url_for, flash, jsonify


app = Flask(__name__)

engine = create_engine("sqlite:///restaurantmenu.db")
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


# API endpoint for restaurant menu (GET Request)
@app.route("/restaurants/<int:restaurant_id>/menu/JSON/")
def restaurant_menu_json(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    menu_items = restaurant.menu_items
    return jsonify(MenuItems=[i.serialize for i in menu_items])


# API endpoint for menu item (GET Request)
@app.route("/restaurants/<int:restaurant_id>/menu/<int:menu_id>/JSON/")
def menu_item_json(restaurant_id, menu_id):
    menu_item = session.query(MenuItem).filter_by(id=menu_id).one()
    return jsonify(MenuItem=menu_item.serialize)


@app.route("/")
@app.route("/restaurants/<int:restaurant_id>/")
def restaurant_menu(restaurant_id):
    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    menu_items = restaurant.menu_items
    return render_template(
        'menu.html',
        restaurant=restaurant,
        items=menu_items
    )


@app.route(
    "/restaurants/<int:restaurant_id>/new/",
    methods=["GET", "POST"]
)
def new_menu_item(restaurant_id):
    if request.method == "POST":
        new_item = MenuItem(
            name=request.form["name"],
            restaurant_id=restaurant_id
        )
        session.add(new_item)
        session.commit()
        flash("new menu item created!")
        return redirect(url_for(
            'restaurant_menu',
            restaurant_id=restaurant_id
        ))

    restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
    return render_template('new_menu_item.html', restaurant=restaurant)


@app.route(
    "/restaurants/<int:restaurant_id>/<int:menu_id>/edit/",
    methods=["GET", "POST"]
)
def edit_menu_item(restaurant_id, menu_id):
    if request.method == "POST":
        new_name = request.form["name"]
        menu_item = session.query(MenuItem) \
                        .filter_by(id=menu_id) \
                        .one()
        menu_item.name = new_name
        session.add(menu_item)
        session.commit()
        flash("menu item edited!")
        return redirect(url_for(
            'restaurant_menu',
            restaurant_id=restaurant_id
        ))


    menu_item = session.query(MenuItem).filter_by(id=menu_id).one()
    restaurant = menu_item.restaurant
    return render_template(
        'edit_menu_item.html',
        restaurant=restaurant,
        menu_item=menu_item
    )


@app.route(
    "/restaurants/<int:restaurant_id>/<int:menu_id>/delete/",
    methods=["GET", "POST"]
)
def delete_menu_item(restaurant_id, menu_id):
    if request.method == "POST":
        menu_item = session.query(MenuItem) \
                        .filter_by(id=menu_id) \
                        .one()
        session.delete(menu_item)
        session.commit()
        flash("menu item deleted!")
        return redirect(url_for(
            'restaurant_menu',
            restaurant_id=restaurant_id
        ))

    menu_item = session.query(MenuItem).filter_by(id=menu_id).one()
    restaurant = menu_item.restaurant
    return render_template(
        'delete_menu_item.html',
        restaurant=restaurant,
        menu_item=menu_item
    )


if __name__ == "__main__":
    app.secret_key = "super_secret_key"
    app.debug = True
    app.run(host="0.0.0.0", port=5000)
