from django import template
from promrep.models import PostAssertion

register = template.Library()


@register.inclusion_tag('promrep/tags/office_badges.html', takes_context=True)
def get_office_badges(context, person_id):
    offices = None
    selected_offices = context.get('selected_offices')

    if selected_offices:
        offices = PostAssertion.objects.filter(
            person_id=person_id,
            office__name__in=selected_offices).order_by('date_start')

    return {'office_badges': offices}


def find_date(year_list, search_year):
    for year in year_list:
        if int(year['grouper']) == search_year:
            return year
    return None


# Deprecated, but left in for now.
@register.simple_tag(takes_context=True)
def merge_out_of_year_range(context, year_list):
    """ Add multi-year offices that begin before a search range to the first/last
    year of that range."""
    if context.get('request').GET:
        if 'date_from' in context.get('request').GET:
            date_from = context.get('request').GET['date_from']
        else:
            date_from = None
        if 'date_to' in context.get('request').GET:
            date_to = context.get('request').GET['date_to']
        else:
            date_to = None
        if date_from or date_to:
            if date_from:
                date_from = int(date_from) * -1
                date_from_index = find_date(year_list, date_from)
            if date_to:
                date_to = int(date_to) * -1
                date_to_index = find_date(year_list, date_to)
            new_year_list = list()
            for year in year_list:
                if (date_from and int(year['grouper']) <= date_from) or \
                        (date_to and int(year['grouper']) >= date_to):
                    if date_from and int(year['grouper']) <= date_from:
                        date_from_index['list'] = date_from_index[
                            'list'] + year['list']
                    elif date_to and int(year['grouper']) >= date_to:
                        date_to_index['list'] = date_to_index[
                            'list'] + year['list']
                else:
                    new_year_list.append(year)
            return new_year_list
    return year_list
