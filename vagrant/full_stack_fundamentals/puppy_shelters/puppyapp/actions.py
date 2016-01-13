from random import choice
from .models import Puppy, Adopter, Shelter
from .db import session


def transfer_puppy(puppy, new_shelter, old_shelter=None):
    puppy.shelter_id = new_shelter.id
    new_shelter.current_occupancy += 1
    session.add_all([puppy, new_shelter])
    if old_shelter:
        old_shelter.current_occupancy -= 1
        session.add(old_shelter)
    if len(puppy.adopters):
        del puppy.adopters[:]
    session.commit()


def check_in_puppy(puppy, shelter=None):
    """
    Checks puppy into open shelter (the supplied one, if given and open).

    Args:
      puppy: the Puppy instance to check into the shelter
      shelter: the Shelter where we intend to house the Puppy

    Returns:
      A status message indicating the shelter where the puppy was
      checked in. If all shelters were full, the message will
      indicate that the puppy was not successfully checked in.
    """
    if shelter and puppy.shelter_id and puppy.shelter_id == shelter.id:
        return puppy.name + " was already checked into " + shelter.name + "."

    open_shelters = session.query(Shelter).filter(
        Shelter.current_occupancy < Shelter.maximum_capacity
    ).all()

    if len(open_shelters) == 0:
        return "No shelter has room to take in " + puppy.name + "!"

    if shelter and shelter in open_shelters:
        transfer_puppy(puppy, shelter, puppy.shelter)
        return puppy.name + " was checked into " + shelter.name + "."
    
    # a shelter is randomly chosen from among all shelters sharing
    # the lowest occupancy count, so as to balance capacity but also avoid
    # distribution bias
    minimum_occupancy = min([s.current_occupancy for s in open_shelters])
    new_shelter = choice(filter(
        lambda s: s.current_occupancy == minimum_occupancy,
        open_shelters
    ))
    transfer_puppy(puppy, new_shelter, puppy.shelter)

    if shelter:
        return shelter.name + " was beyond capacity, so " + puppy.name + \
            " was checked into " + new_shelter.name + "."

    return puppy.name + " was checked into " + new_shelter.name + "."


def process_puppy_adoption(puppy_id, adopter_ids):
    """
    Has puppy with given id adopted by adopters with given ids.
    Also removes exisiting relationships.

    Args:
      puppy_id: the id of the puppy to be adopted
      adopter_ids: a list of ids belonging to adopters

    Returns:
      A status message indicating who adopted the puppy.
    """
    puppy = session.query(Puppy).filter_by(id=puppy_id).one()
    adopters = session.query(Adopter).filter(Adopter.id.in_(adopter_ids)).all()
    old_adopters = puppy.adopters
    old_shelter = puppy.shelter
    puppy.shelter = None
    del puppy.adopters[:]
    if old_shelter:
        old_shelter.current_occupancy -= 1
        session.add(old_shelter)
    puppy.adopters.extend(adopters)
    session.add(puppy)
    session.commit()
    adopter_names = [a.name for a in adopters]
    return puppy.name + " was adopted by " + ", ".join(adopter_names)
