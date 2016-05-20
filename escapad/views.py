#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import mimetypes
import os.path
import subprocess

from django.conf import settings
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import View

from .models import Repository

# Create your views here.


def index(request):
    return HttpResponse(u"Liste des dépôt")



def build_repo(request, username, name):
    return HttpResponse(u"Building repo user = %s | name = %s" % (username, name))

class BuildView(View):
    """
    A view for generating site from Repository
    """

    def post(self, request, username, name, *args, **kwargs):
        pass



def visit_site(request, username, name):
    return HttpResponse(u"Visiting site for repo user = %s | name = %s" % (username, name))
