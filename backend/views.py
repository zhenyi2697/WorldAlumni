# -- encoding:utf-8 --

import datetime
from django.utils import timezone
from functools import wraps
import json
import zipfile

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import Http404
from django.contrib.auth import logout as user_logout
from django.shortcuts import render
from django.template import RequestContext
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings


def home(request):
    ''' home page for website'''

    bindingId = '-1'
    if request.user.is_authenticated():
        bindings = request.user.binding_set.all()
        if len(bindings) == 0:
            bindingId = '-1'
        elif len(bindings) == 1:
            bindingId = bindings[0].id
        elif len(bindings) == 2:
            if bindings[0].bind_from == 'facebook': ### if two bindings, find the one with facebook
                bindingId = bindings[0].id
            else:
                bindingId = bindings[1].id

    return render(request, 'home.html', {'bindingId': bindingId})

def logout(request):
    ''' logout of website'''
    user_logout(request)
    return HttpResponseRedirect("/")



