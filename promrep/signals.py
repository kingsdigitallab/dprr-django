from promrep.models import Post, PostAssertion
from django.db.models.signals import post_delete

def delete_parent_post(sender, instance, *args, **kwargs):
    """
    deletes the post associated with a post assertion if
    that post only has that post assertion
    """

    if instance.post.postassertion_set.count() == 0:
        instance.post.delete()

post_delete.connect(delete_parent_post, sender=PostAssertion)