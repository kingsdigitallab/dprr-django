from promrep.models import Group, PostAssertion
from django.db.models.signals import post_delete

def delete_parent_group(sender, instance, *args, **kwargs):
    """
    deletes the group associated with a post assertion if
    that post only has that post assertion
    """

    if instance.group:
        if instance.group.postassertion_set.count() == 0:
            instance.group.delete()

post_delete.connect(delete_parent_group, sender=PostAssertion)
