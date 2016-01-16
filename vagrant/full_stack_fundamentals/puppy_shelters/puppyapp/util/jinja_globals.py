def get_default_attr_dict(obj, attr_name):
    """
    Returns a dictionary made of an attribute's default value (if present),
    given an object and the desired attribute name.

    Allows splat expansion of dictionary in a macro call into keyword
    arguments, so that if the dictionary is empty, no keyword argument
    is passed.

    i.e. `**get_default_attr_dict(obj, attr_name)`

    Args:
      obj: db.Model - the object that may contain the desired attribute
      attr_name: str - the name of the desired attribute

    Returns:
      dict - a dictionary wrapping the "value" key and attribute value,
      or an empty dictionary, if the value doesn't exist or is None. 
    """

    if obj and hasattr(obj, attr_name) and getattr(obj, attr_name):
        return {"value": getattr(obj, attr_name)}

    return {}


global_fns = [get_default_attr_dict]
