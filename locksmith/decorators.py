__author__ = 'michal'

from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from django.http.response import HttpResponseForbidden
from .models import Key
import json


def key_required(key_name: str, redirect_url=None, json_response={}):
    """
    Checks if the logged user as access to this view
    if it has the keychain for it

    :param keychain_name:
    :return:
    """

    def decorator(view):
        nonlocal key_name

        def wrapped_view(request, *args, **kwargs):
            try:
                if not request.user.is_authenticated():
                    raise PermissionDenied
                keychain = request.user.keychain
                if (key_name in keychain and
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