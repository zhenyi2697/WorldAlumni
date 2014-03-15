# -- encoding:utf-8 --

import datetime
from django.utils import timezone
from functools import wraps
import json
import zipfile

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import Http404
from django.shortcuts import render
from django.template import RequestContext
from django.core.exceptions import PermissionDenied, ObjectDoesNotExist
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.conf import settings

def home(request):
    ''' home page for website'''

    return render(request, 'home.html', {})

