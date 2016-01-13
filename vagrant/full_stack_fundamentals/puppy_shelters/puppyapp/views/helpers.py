from flask import request
from math import ceil
from ..db import session


ITEMS_PER_PAGE = 10


def get_number_of_pages(data_class):
    """
    given SQLAlchemy class, returns number of pages to display all instances

    Args:
      data_class: SQLAlchemy class - of which instances will be counted

    Returns:
      int - number of pages required to display all instances
    """

    number_of_pages = int(ceil(
        session.query(data_class).count() / (ITEMS_PER_PAGE*1.0)
    ))
    return number_of_pages


def get_current_page(pagelimit):
    """
    given a page limit, and using the 'p' query argument, gets current page.

    Args:
      pagelimit: int - maximum page value that can be returned

    Returns:
      int - current page number
    """
    p = request.args.get("p")
    current_page = min(p and int(p) or 1, pagelimit)
    return current_page
