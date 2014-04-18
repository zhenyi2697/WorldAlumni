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

from backend.models import *

DISTANCE_ONLY_ENTRY = 1
INVISIBLE_ENTRY = 2

def is_invisible(binding):
    invisible = 0
    try:
        invisible_setting = UserSetting.objects.get(user=binding.user, entry=INVISIBLE_ENTRY)
        if invisible_setting.value == 1:
            invisible = 1
    except UserSetting.DoesNotExist:
        pass
    return invisible

def is_distance_only(binding):
    distance_only = 0
    try:
        distance_only_setting = UserSetting.objects.get(user=binding.user, entry=DISTANCE_ONLY_ENTRY)
        if distance_only_setting.value == 1:
            distance_only = 1
    except UserSetting.DoesNotExist:
        pass

    return distance_only

def home(request):
    ''' home page for website'''

    bindingId = '-1'
    binding = None
    if request.user.is_authenticated():
        bindings = request.user.binding_set.all()
        if len(bindings) == 0:
            bindingId = '-1'
        elif len(bindings) == 1:
            bindingId = bindings[0].id
            binding = bindings[0]
        elif len(bindings) == 2:
            if bindings[0].bind_from == 'facebook': ### if two bindings, find the one with facebook
                bindingId = bindings[0].id
                binding = bindings[0]
            else:
                bindingId = bindings[1].id
                binding = bindings[1]

    distance_only = False
    invisible = False

    if binding:
        distance_only = is_distance_only(binding)
        invisible = is_invisible(binding)

    return render(request, 'home.html', {'bindingId': bindingId, 'distance_only': distance_only, 'invisible': invisible})

def logout(request):
    ''' logout of website'''
    user_logout(request)
    return HttpResponseRedirect("/")



