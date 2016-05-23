#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import mimetypes
import os.path
import subprocess
import logging

from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.views.generic import View

from .models import Repository

logger = logging.getLogger(__name__)
# Create your views here.

def index(request):
    return HttpResponse(u"Liste des dépôt")

class BuildView(View):
    """
    A view for generating site from Repository
    """
    
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(BuildView, self).dispatch(*args, **kwargs)

    def post(self, request, username, name, *args, **kwargs):
        logger.warn("Post to buidl view !")
        
        return JsonResponse({"success":"true"})


def visit_site(request, username, name):
    return HttpResponse(u"Visiting site for repo user = %s | name = %s" % (username, name))
