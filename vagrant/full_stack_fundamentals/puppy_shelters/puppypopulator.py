"""
Populates existing database from puppyapp with data
(assumes presence of a flask.ctx.AppContext instance when run)
"""

from flask.ext.sqlalchemy import SQLAlchemy
from puppyapp import app, db
from puppyapp.models import Shelter, Puppy, PuppyProfile, Adopter
import datetime
import random


def populate():
    """
    populates the puppies database with instances of Puppy, Shelter, Adopter
    """

    #Add Shelters
    shelters = []

    shelter1 = Shelter(name = "Oakland Animal Services", address = "1101 29th Ave", city = "Oakland", state = "California", zip_code = "94601", website = "http://oaklandanimalservices.org", maximum_capacity=22)
    shelters.append(shelter1)
    db.session.add(shelter1)

    shelter2 = Shelter(name = "San Francisco SPCA Mission Adoption Center", address="250 Florida St", city="San Francisco", state="California", zip_code = "94103", website = "http://sfspca.org", maximum_capacity=22)
    shelters.append(shelter2)
    db.session.add(shelter2)

    shelter3 = Shelter(name = "Wonder Dog Rescue", address= "2926 16th Street", city = "San Francisco", state = "California" , zip_code = "94103", website = "http://wonderdogrescue.org", maximum_capacity=22)
    shelters.append(shelter3)
    db.session.add(shelter3)

    shelter4 = Shelter(name = "Humane Society of Alameda", address = "PO Box 1571" ,city = "Alameda" ,state = "California", zip_code = "94501", website = "http://hsalameda.org", maximum_capacity=22)
    shelters.append(shelter4)
    db.session.add(shelter4)

    shelter5 = Shelter(name = "Palo Alto Humane Society" ,address = "1149 Chestnut St." ,city = "Menlo Park", state = "California" ,zip_code = "94025", website = "http://paloaltohumane.org", maximum_capacity=22)
    shelters.append(shelter5)
    db.session.add(shelter5)


    #Add Puppies

    male_names = ["Bailey", "Max", "Charlie", "Buddy","Rocky","Jake", "Jack", "Toby", "Cody", "Buster", "Duke", "Cooper", "Riley", "Harley", "Bear", "Tucker", "Murphy", "Lucky", "Oliver", "Sam", "Oscar", "Teddy", "Winston", "Sammy", "Rusty", "Shadow", "Gizmo", "Bentley", "Zeus", "Jackson", "Baxter", "Bandit", "Gus", "Samson", "Milo", "Rudy", "Louie", "Hunter", "Casey", "Rocco", "Sparky", "Joey", "Bruno", "Beau", "Dakota", "Maximus", "Romeo", "Boomer", "Luke", "Henry"]

    female_names = ['Bella', 'Lucy', 'Molly', 'Daisy', 'Maggie', 'Sophie', 'Sadie', 'Chloe', 'Bailey', 'Lola', 'Zoe', 'Abby', 'Ginger', 'Roxy', 'Gracie', 'Coco', 'Sasha', 'Lily', 'Angel', 'Princess','Emma', 'Annie', 'Rosie', 'Ruby', 'Lady', 'Missy', 'Lilly', 'Mia', 'Katie', 'Zoey', 'Madison', 'Stella', 'Penny', 'Belle', 'Casey', 'Samantha', 'Holly', 'Lexi', 'Lulu', 'Brandy', 'Jasmine', 'Shelby', 'Sandy', 'Roxie', 'Pepper', 'Heidi', 'Luna', 'Dixie', 'Honey', 'Dakota']

    puppy_images = ["http://pixabay.com/get/da0c8c7e4aa09ba3a353/1433170694/dog-785193_1280.jpg?direct", "http://pixabay.com/get/6540c0052781e8d21783/1433170742/dog-280332_1280.jpg?direct","http://pixabay.com/get/8f62ce526ed56cd16e57/1433170768/pug-690566_1280.jpg?direct","http://pixabay.com/get/be6ebb661e44f929e04e/1433170798/pet-423398_1280.jpg?direct","http://pixabay.com/static/uploads/photo/2010/12/13/10/20/beagle-puppy-2681_640.jpg","http://pixabay.com/get/4b1799cb4e3f03684b69/1433170894/dog-589002_1280.jpg?direct","http://pixabay.com/get/3157a0395f9959b7a000/1433170921/puppy-384647_1280.jpg?direct","http://pixabay.com/get/2a11ff73f38324166ac6/1433170950/puppy-742620_1280.jpg?direct","http://pixabay.com/get/7dcd78e779f8110ca876/1433170979/dog-710013_1280.jpg?direct","http://pixabay.com/get/31d494632fa1c64a7225/1433171005/dog-668940_1280.jpg?direct"]

    descriptions = ["Loves to walk", "Loves to swim", "Loves to fly"]

    special_needs_lists = ["Care, affection, love", "Darkness, fear, loathing", "Sparkles, ice cream, rainbows"]

    # Adopter names

    adopter_names = ['Joe', 'Darth', 'Jane', 'Dax', 'Jax', '#YOLO', 'Grimes', 'Yoda', 'Asana']

    #This method will make a random age for each puppy between 0-18 months(approx.) old from the day the algorithm was run.
    def CreateRandomAge():
        today = datetime.date.today()
        days_old = random.randint(0,540)
        birthday = today - datetime.timedelta(days = days_old)
        return birthday

    #This method will create a random weight between 1.0-40.0 pounds (or whatever unit of measure you prefer)
    #results will be rounded to nearest tenth (0.1)
    def CreateRandomWeight():
        return round(random.uniform(1.0, 40.0) / 0.1) * 0.1

    adopters = []
    for i,x in enumerate(adopter_names):
        adopter = Adopter(name=x)
        adopters.append(adopter)
        db.session.add(adopter)

    for i,x in enumerate(male_names):
        random_shelter_id = random.randint(1, 5)
        random_shelter = shelters[random_shelter_id - 1]
        while(random_shelter.current_occupancy >= random_shelter.maximum_capacity):
            random_shelter_id = random.randint(1, 5)
            random_shelter = shelters[random_shelter_id - 1]

        new_puppy = Puppy(name = x, gender = "male", date_of_birth = CreateRandomAge(),shelter_id=random_shelter_id, weight_lbs= CreateRandomWeight())
        random_shelter.current_occupancy += 1
        new_profile = PuppyProfile(picture="http://loremflickr.com/500/375/cute,puppy", description=random.choice(descriptions), special_needs=random.choice(special_needs_lists))
        new_puppy.profile = new_profile
        for a in adopters:
            if random.randint(0, 1) == 1:
                new_puppy.adopters.append(a)

        db.session.add(new_puppy)
        db.session.add(new_profile)

    for i,x in enumerate(female_names):
        random_shelter_id = random.randint(1, 5)
        random_shelter = shelters[random_shelter_id - 1]
        while(random_shelter.current_occupancy >= random_shelter.maximum_capacity):
            random_shelter_id = random.randint(1, 5)
            random_shelter = shelters[random_shelter_id - 1]

        new_puppy = Puppy(name = x, gender = "female", date_of_birth = CreateRandomAge(),shelter_id=random_shelter_id, weight_lbs= CreateRandomWeight())
        random_shelter.current_occupancy += 1
        new_profile = PuppyProfile(picture="http://loremflickr.com/500/375/cute,puppy", description=random.choice(descriptions), special_needs=random.choice(special_needs_lists))
        new_puppy.profile = new_profile
        for a in adopters:
            if random.randint(0, 1) == 1:
                new_puppy.adopters.append(a)

        db.session.add(new_puppy)
        db.session.add(new_profile)

    db.session.commit()
