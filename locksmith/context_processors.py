__author__ = 'michal'
from .models import Key


def checks(request):

    def user_has_key(keyname):
        nonlocal request

        return (Key.get(name=keyname) in request.user.keychain and
                request.user.keychain.is_expired())

    return {
        "locksmith_user_has_key": user_has_key
    }