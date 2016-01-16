def names(obj_list):
    """
    maps lists of Puppy, Shelter, or Adopter objects
    to lists of names; used as Jinja filter
    """

    return [o.name for o in obj_list]


filters = [names]
