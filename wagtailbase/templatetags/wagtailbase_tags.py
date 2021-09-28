import logging

from django import template
from django.conf import settings
from django.template.defaultfilters import stringfilter
from django.utils.text import slugify
from wagtail.contrib.routable_page.templatetags.wagtailroutablepage_tags import (
    routablepageurl,
)
from wagtail.core.models import Page
from wagtail.core.templatetags.wagtailcore_tags import pageurl
from wagtailbase.util import unslugify
from wagtail.core.models import Site

from ..models import BlogPost, HomePage

logger = logging.getLogger(__name__)

register = template.Library()


@register.simple_tag
def url_replace(request, field, value):
    dict_ = request.GET.copy()
    dict_[field] = value
    return dict_.urlencode()


@register.inclusion_tag("wagtailbase/tags/breadcrumbs.html", takes_context=True)
def breadcrumbs(context, root, current_page, extra=None):
    """Returns the pages that are part of the breadcrumb trail of the current
    page, up to the root page."""
    pages = (
        current_page.get_ancestors(
            inclusive=True
        ).descendant_of(root).filter(live=True)
    )

    return {
        "request": context["request"],
        "root": root,
        "current_page": current_page,
        "pages": pages,
        "extra": extra,
    }


@register.simple_tag(takes_context=False)
def are_comments_allowed():
    """Returns True if commenting on the site is allowed, False otherwise."""
    return getattr(settings, "ALLOW_COMMENTS", False)


@register.simple_tag(takes_context=False)
def get_disqus_shortname():
    """Returns the DISCUS shortname setting for comments."""
    return settings.DISQUS_SHORTNAME


@register.simple_tag(takes_context=True)
def get_request_parameters(context, exclude=None):
    """Returns a string with all the request parameters except the exclude
    parameter."""
    params = ""
    request = context["request"]

    for key, value in list(request.GET.items()):
        if key != exclude:
            for val in request.GET.getlist(key):
                params += "&{key}={value}".format(key=key, value=val)

    return params


@register.simple_tag(takes_context=True)
def get_site_root(context):
    """Returns the site root Page, not the implementation-specific model used.

    :rtype: `wagtail.core.models.Page`
    """
    return Site.find_for_request(context["request"]).root_page


@register.simple_tag(takes_context=True)
def has_local_menu(context, current_page):
    """Returns True if the current page has a local menu, False otherwise. A
    page has a local menu, if it is not the site root, and if it is not a leaf
    page."""
    site_root = get_site_root(context)

    try:
        current_page.id
    except AttributeError:
        return False

    if current_page.id != site_root.id:
        if current_page.depth <= 4 and not current_page.is_leaf():
            return True
        elif current_page.depth > 4:
            return True

    return False


@register.filter
def is_current_or_ancestor(page, current_page):
    """Returns True if the given page is the current page or is an ancestor of
    the current page."""
    return current_page.is_current_or_ancestor(page)


@register.inclusion_tag("wagtailbase/tags/latest_blog_post.html", takes_context=True)
def latest_blog_post(context, parent=None):
    """Returns the latest blog post that is child of the given parent. If no
    parent is given it defaults to the latest BlogPost object."""
    post = None

    if parent:
        post = parent.posts.order_by("-date").first()
    else:
        post = BlogPost.objects.filter(live=True).order_by("-date").first()

    return {"request": context["request"], "post": post}


@register.inclusion_tag("wagtailbase/tags/featured_blog_post.html", takes_context=True)
def featured_blog_post(context, parent=None):
    """Returns the latest featured blog post that is child of the given parent.
    If no parent is given it defaults to the latest featured BlogPost object.
    """
    post = None
    if parent:
        post = parent.posts.filter(featured=True).order_by("-date").first()
    else:
        post = BlogPost.objects.filter(featured=True).order_by("-date").first()

    return {"request": context["request"], "post": post}


@register.inclusion_tag("wagtailbase/tags/latest_n_blog_posts.html", takes_context=True)
def latest_n_blog_posts(context, nentries, parent=None):
    """Returns an array with the latest blog posts that are children of the
    given parent. The number of blog posts is specified in nentries. If
    there are not enough blog posts, it returns all the existing entries.
    If no parent is given it defaults to the latest BlogPost object."""

    posts = []
    base_model = BlogPost

    if parent:
        base_model = parent

    posts = base_model.objects.all().order_by("-date")[0:nentries]

    return {"request": context["request"], "posts": posts}


@register.inclusion_tag("wagtailbase/tags/local_menu.html", takes_context=True)
def local_menu(context, current_page=None):
    """Retrieves the secondary links for the 'also in this section' links -
    either the children or siblings of the current page."""
    menu_pages = []
    label = current_page.title

    if current_page:
        menu_pages = current_page.get_children().filter(live=True, show_in_menus=True)

        # if no children, get siblings instead
        if len(menu_pages) == 0:
            menu_pages = current_page.get_siblings().filter(
                live=True, show_in_menus=True
            )

        if current_page.get_children_count() == 0:
            if not isinstance(current_page.get_parent().specific, HomePage):
                label = current_page.get_parent().title

    # required by the pageurl tag that we want to use within this template
    return {
        "request": context["request"],
        "current_page": current_page,
        "menu_pages": menu_pages,
        "menu_label": label,
    }


def has_menu_children(page):
    return page.get_children().live().in_menu().exists()


# Retrieves the top menu items - the immediate children of the parent page
# The has_menu_children method is necessary because the template requires
# a dropdown class to be applied to a parent
#
# adapted from
#   github.com/torchbox/wagtaildemo/blob/master/demo/templatetags/demo_tags.py


@register.inclusion_tag("wagtailbase/tags/main_menu.html", takes_context=True)
def main_menu(context, root, current_page=None):
    """Returns the main menu items, the children of the root page. Only live
    pages that have the show_in_menus setting on are returned."""
    menu_pages = root.get_children().filter(live=True, show_in_menus=True)

    for menu_page in menu_pages:
        menu_page.show_dropdown = has_menu_children(menu_page)

    return {
        "request": context["request"],
        "root": root,
        "current_page": current_page,
        "menu_pages": menu_pages,
    }


# Retrieves the children of the top menu items for the drop downs


@register.inclusion_tag("wagtailbase/tags/top_menu_children.html", takes_context=True)
def top_menu_children(context, parent):
    menuitems_children = parent.get_children()
    menuitems_children = menuitems_children.live().in_menu()
    return {
        "parent": parent,
        "menuitems_children": menuitems_children,
        # required by the pageurl tag that we want to use within this template
        "request": context["request"],
    }


@register.simple_tag(takes_context=True)
def slugurl(context, slug):
    """Returns the URL for the page that has the given slug."""
    page = Page.objects.filter(slug=slug).first()

    if page:
        return pageurl(context, page)
    else:
        return None


@register.simple_tag(takes_context=True)
def archiveurl(context, page, *args):
    """[DEPRECATED] Returns the URL for the page that has the given slug.
    Use routablepageurl from wagtail.contrib.routable_page templatetag
    instead.

    for example:
        `{% archiveurl page author %}`

        should be:
        `{% routablepageurl page 'author' author %}`
    """

    logger.warning(
        (
            "DEPRECATED: wagtailbase tag archiveurl is depracated. "
            "Use routablepageurl from wagtail.contrib.routable_page "
            "templatetag instead."
        )
    )

    try:
        url_name = "author"
        a_args = [slugify(args[0].username)]
    except AttributeError:
        try:
            url_name = "tag"
            a_args = [slugify(args[0].name)]
        except AttributeError:
            url_name = "date"
            a_args = args

    except IndexError:
        url_name = ""
        a_args = []

    return routablepageurl(context, page.specific, url_name, *a_args)


@register.filter(name="unslugify")
@stringfilter
def unslugify_filter(value):
    return unslugify(value)


@register.filter
def get_item(dictionary, key):
    if dictionary:
        return dictionary[key]

    return None


@register.filter(name="lookup")
def lookup(dict, index):
    # used to lookup keys in dictionary
    #  useful to use variables in templates
    # differs from get item as it checks if key exists

    if index in dict:
        return dict[index]
    return ""


@register.simple_tag(takes_context=True)
def dprr_has_local_menu(context, current_page):
    """Returns True if the current page has a local menu, False otherwise. A
    page has a local menu, if it is not the site root or first level,
    unless it has children page.
    """

    try:
        current_page.id
    except AttributeError:
        return False

    # Level 3 corresponds to top navigation and level 4 to sub-nav
    if current_page.depth >= 3 and not current_page.is_leaf():
        return True
    elif current_page.depth >= 4:
        return True

    return False


@register.simple_tag(takes_context=True)
def select_facet_link(context, facetname, option):
    query = context["request"].GET.copy()

    if "selected_facets" in query:
        query.update({"selected_facets": facetname + ":" + option})
    else:
        query["selected_facets"] = facetname + ":" + option

    if "page" in query:
        del query["page"]
    if "printme" in query:
        del query["printme"]

    return "?" + query.urlencode(safe=":?")
