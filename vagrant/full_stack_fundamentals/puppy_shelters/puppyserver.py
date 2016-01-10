from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database_setup import Base, Shelter, Puppy, PuppyProfile, Adopter
from flask import Flask, request, redirect, render_template, url_for, flash, jsonify


app = Flask(__name__)

engine = create_engine("sqlite:///puppies.db")
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()


#PUPPY SPECIFIC OPERATIONS

#/, /puppies/ (R)
#Puppies List view


#/puppies/new/ (C)
#Register new puppy


#/puppies/<int:puppy_id>/ (R)
#View full profile of puppy with matching puppy_id


#/puppies/<int:puppy_id>/edit/ (U)
#Edit info for puppy with matching puppy_id


#/puppies/<int:puppy_id>/delete/ (D)
#Delete puppy with matching puppy_id


#PUPPY TRANSACTION OPERATIONS

#/puppies/<int:puppy_id>/switch_shelter/
#Check puppy into a new shelter


#/puppies/<int:puppy_id>/adopt/
#Turn over puppy to one or more adopters


#ADOPTER SPECIFIC OPERATIONS

#/adopters/ (R)
#Adopters list view


#/adopters/new/ (C)
#Register new adopter


#/adopters/<int:adopter_id>/ (R)
#View full profile of adopter with matching adopter_id


#/adopters/<int:adopter_id>/edit/ (U)
#Edit info for adopter with matching adopter_id


#/adopters/<int:adopter_id/delete/ (D)
#Delete adopter with matching adopter_id


#SHELTER SPECIFIC OPERATIONS

#/shelters/ (R)
#Shelters list view


#/shelters/new/ (C)
#Register new shelter


#/shelters/<int:shelter_id>/ (R)
#View full profile of shelter with matching shelter_id


#/shelters/<int:shelter_id>/edit/ (U)
#Edit info for shelter with matching shelter_id


#/shelters/<int:shelter_id/delete/ (D)
#Delete shelter with matching shelter_id


if __name__ == "__main__":
    app.secret_key = "super_secret_key"
    app.debug = True
    app.run(host="0.0.0.0", port=5000)
