from django.conf import settings
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator


def create_pagination(results, results_per_page, page_number):
    """Returns a Paginator and Page for `results`.

    This function handles various possible problems with
    `page_number`, as per the example view code in the Django
    documentation.

    :param results: results to be paginated
    :type results: `django.db.models.query.QuerySet` or `list`
    :param results_per_page: number of results to display per page
    :type results_per_page: `int`
    :param page_number: number of current page
    :type page_number: `int`
    :rtype: `tuple` of `django.core.paginator.Paginator`,
            `django.core.paginator.Page`

    """
    paginator = Paginator(results, results_per_page)
    try:
        page = paginator.page(page_number)
    except PageNotAnInteger:
        page = paginator.page(1)
    except EmptyPage:
        page = paginator.page(paginator.num_pages)
    return paginator, page


class PaginationDisplay (object):

    """Class for generating data from which a full set of links to a
    paginated set of items may be easily rendered.

    The display consists of the following (in order):

    * A link to the previous item, if `page` is not the first.

    * Links to the first X pages, up to at most `page`.

    * An ellipsis, if the Xth page is not followed either by `page` or
      its Y preceding pages.

    * Links to up to Y pages immediately preceding `page`, if they do
      not overlap with the first X pages.

    * The current page.

    * Links to up to Y pages immediately following `page`.

    * An ellipsis, if the Yth following page is more than X pages from
      the last page.

    * Links to the last X pages, if they do not overlap with any pages
      listed previously.

    * A link to the next item, if `page` is not the last.

    The values of X and Y can be set in the settings module, using the
    attributes PAGINATION_DISPLAY_END_COUNT and
    PAGINATION_DISPLAY_NEAR_COUNT respectively.

    """

    def __init__(self, querydict):
        self._qd = querydict.copy()

    def _get_data(self, text, classes, number=None, title=None):
        """Returns a tuple of data representing an item to be displayed.

        :param text: the text of the item
        :type text: `str`
        :param classes: classes to apply to the item
        :type classes: `list`
        :param number: the number of the page this item refers to
        :type number: `int`
        :param title: the title of the item
        :type title: `str`
        :rtype: `tuple`

        """
        url = ''
        if number:
            self._qd['page'] = number
            url = '?{0}'.format(self._qd.urlencode())
        return (classes, url, text, title)

    def generate_data(self, page):
        """Returns a list of tuples representing the sequence of items to be
        displayed linking pages in the results, from the context of
        `page`.

        Each tuple consists of a list of class names, the URL
        destination (may be an empty string), the text, and the
        title. There is no HTML markup present; the elements are
        intended to be constructed into HTML (or even something else)
        in a template.

        :param page: context page of a set of paginated results
        :type page: `django.core.paginator.Page`
        :rtype: `list` of `tuple`

        """
        paginator = page.paginator
        page_range = list(paginator.page_range)
        last = paginator.num_pages
        data = []
        current = page.number
        context = current - 1  # The list index of the current page
        # Number of pages to display at the start and end of the list.
        try:
            end_count = settings.PAGINATION_DISPLAY_END_COUNT
        except AttributeError:
            end_count = 2
        # Number of pages immediately before and after current page to
        # display.
        try:
            near_count = settings.PAGINATION_DISPLAY_NEAR_COUNT
        except AttributeError:
            near_count = 3
        if current > 1:
            # Add a link to the previous page.
            data.append(self._get_data('&laquo;', ['arrow'], current - 1,
                                       'Previous'))
            # Add links to the first pages.
            start = min(end_count, context)
            for number in page_range[0:start]:
                data.append(self._get_data(number, [], number))
            if start + near_count < context:
                # Add an elipsis to show the gap between the first and
                # the preceding pages.
                data.append(self._get_data('&hellip;', ['unavailable']))
            for number in page_range[
                    max(start, context - near_count):context]:
                data.append(self._get_data(number, [], number))
        # Add the current page.
        data.append(self._get_data(current, ['current'], current))
        if page.has_next():
            # Add links to the following pages.
            for number in list(
                    page_range)[context + 1:context + 1 + near_count]:
                data.append(self._get_data(number, [], number))
            end = last - context - 1 - near_count
            if end > end_count:
                # Add an ellipsis to show the gap between the
                # following and the last pages.
                data.append(self._get_data('&hellip;', ['unavailable']))
            if end > 0:
                # Add links to the last pages.
                for number in list(page_range)[-min(end, end_count):]:
                    data.append(self._get_data(number, [], number))
            # Add a link to the next page.
            data.append(self._get_data(
                '&raquo;', ['arrow'], current + 1, 'Next'))
        return data
