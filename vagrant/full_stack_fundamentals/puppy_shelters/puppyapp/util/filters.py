def names(obj_list):
    """
    maps lists of Puppy, Shelter, or Adopter objects
    to lists of names; used as Jinja filter
    """

    return [o.name for o in obj_list]


def one_dec_place(f):
    """
    rounds float or decimal number to one decimal place
    """

    return round(float(f) / 0.1) * 0.1


filters = [names, one_dec_place]
