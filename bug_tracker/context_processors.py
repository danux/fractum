# -*- coding: utf-8 -*-
"""
Adds context processors for the bug tracker app.
"""
from django.conf import settings


def status_constants(request):
    """
    Makes the status constants available in the context.
    :param request: HttpRequest
    :return: {}
    """
    return {
        'status_constants': settings.STATUS_PKS
    }
