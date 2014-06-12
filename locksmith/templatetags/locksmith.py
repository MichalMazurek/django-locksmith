from locksmith.models import Key
from django import template
from django.db.models import ObjectDoesNotExist

register = template.Library()


@register.assignment_tag(takes_context=True)
def user_has_key(context, key_name, *args, **kwargs):

    request = context['request']
    user = request.user
    """:type: models.LocksmithMixin """
    if user.keychain is not None:
        try:
            return bool(key_name in user.keychain and
                        not user.keychain.is_expired())
        except ObjectDoesNotExist:
            return False
    else:
        return False

