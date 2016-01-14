from flask import request
from math import ceil


ITEMS_PER_PAGE = 10


def get_number_of_pages(query):
    """
    given SQLAlchemy query, returns number of pages to display all results

    Args:
      query: SQLAlchemy query - whose results will be counted

    Returns:
      int - number of pages required to display all results
    """

    number_of_pages = int(ceil(query.count() / (ITEMS_PER_PAGE*1.0)))
    return number_of_pages


def get_current_page(pagelimit):
    """
    given a page limit, and using the 'p' query argument, gets current page

    Args:
      pagelimit: int - maximum page value that can be returned

    Returns:
      int - current page number
    """

    p = request.args.get("p")
    current_page = min(p and int(p) or 1, pagelimit)
    return current_page


def get_results_for_current_page(query, order_basis):
    """
    given SQLAlchemy query and order basis, returns model list for current page

    Args:
      query: SQLAlchemy query - which will be filtered for page results
      order_basis: db.Column - the column to use for ordering results

    Returns:
      tuple containing the following:
       - list(db.Model) - the model results to display on the current page
       - int - the current page number
       - int - the total number of pages for this query
    """

    number_of_pages = get_number_of_pages(query)
    page = get_current_page(number_of_pages)
    results =  query.order_by(order_basis) \
                    .offset((page-1) * ITEMS_PER_PAGE) \
                    .limit(ITEMS_PER_PAGE) \
                    .all()
    return (results, page, number_of_pages)
