__author__ = 'michal'

from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from django.http.response import HttpResponseForbidden
from .models import Key, K
import json


def key_required(key_name, redirect_url=None, json_response={}):
    """
    Checks if the logged user as access to this view
    if it has the keychain for it

    :param keychain_name:
    :return:
    """

    def decorator(view):
        nonlocal key_name

        def wrapped_view(request, *args, **kwargs):
            nonlocal key_name
            try:
                if not request.user.is_authenticated():
                    raise PermissionDenied

                if request.user.is_superuser:
                    return view(request, *args, **kwargs)
                keychain = request.user.keychain

                if keychain is None:
                    raise PermissionDenied

                if type(key_name) == str:
                    key_name = K(key_name)

                if (key_name.check_keychain(keychain) and
                        not keychain.is_expired()):
                    return view(request, *args, **kwargs)
                else:
                    return redirect(redirect_url)
            except (Key.DoesNotExist, PermissionDenied):
                if request.is_ajax() and len(json_response) > 0:
                    HttpResponseForbidden(content=json.dumps(json_response),
                                          content_type="application/json")
                elif redirect_url is not None:
                    return redirect(redirect_url)
                else:
                    return HttpResponseForbidden("Permission denied.")
        return wrapped_view

    return decorator