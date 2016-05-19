#!/usr/bin/python
# -*- coding: utf-8 -*-


from django.shortcuts import render
from django.http import HttpResponse


# Create your views here.


def index(request):
    return HttpResponse(u"Liste des dépôt")
    
def build_repo(request, username, name):
    return HttpResponse(u"Building repo user = %s | name = %s" % (username, name))


def visit_site(request, username, name):
    return HttpResponse(u"Visiting site for repo user = %s | name = %s" % (username, name))
