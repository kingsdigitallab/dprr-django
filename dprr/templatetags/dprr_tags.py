
from django import template

import logging
logger = logging.getLogger(__name__)

register = template.Library()

@register.assignment_tag(takes_context=True)
def dprr_has_local_menu(context, current_page):
    """Returns True if the current page has a local menu, False otherwise. A
    page has a local menu, if it is not the site root or first level, unless it has children
    page."""

    try:
        current_page.id
    except AttributeError:
        return False;

    """Level 3 corresponds to top navigation and level 4 to sub-nav"""
    if current_page.depth >= 3 and not current_page.is_leaf():
        return True
    elif current_page.depth >= 4:
        return True

    return False