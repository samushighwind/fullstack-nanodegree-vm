from .. import app

@app.template_filter("names")
def names_filter(obj_list):
    """
    maps lists of Puppy, Shelter, or Adopter objects
    to lists of names; used as Jinja filter
    """

    return [o.name for o in obj_list]


@app.template_filter("one_dec_place")
def one_dec_place_filter(f):
    """
    rounds float or decimal number to one decimal place
    """

    return round(float(f) / 0.1) * 0.1