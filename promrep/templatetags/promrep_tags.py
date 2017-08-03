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
