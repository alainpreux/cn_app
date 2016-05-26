#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import mimetypes
import os.path
import subprocess
import logging
import datetime

from django.conf import settings
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
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
    
    http_method_names = ['get', 'post']
    
    @csrf_exempt
    def dispatch(self, *args, **kwargs):
        return super(BuildView, self).dispatch(*args, **kwargs)
    
    def build_repo(self, slug):
        # 1. cd to repo path
        repo_path = os.path.join(settings.REPOS_DIR, slug)
        build_path = os.path.join(settings.GENERATED_SITES_DIR, slug)
        logger.warn("Post to buidl view ! repo_path = %s" % repo_path)        
        repo_object = Repository.objects.all().filter(slug=slug)[0]
        try:
            os.chdir(repo_path)
        except Exception as e:
            return JsonResponse({"success":"false", "reason":"repo not existing, or not synced"})
        # 2. git pull origin [branch:'master']
        git_cmd = "git pull origin master"
        try:
            subprocess.check_output(git_cmd.split())
        except Exception as e:
            os.chdir(settings.BASE_DIR)
            return JsonResponse({"success":"false", "reason":"error with git pull origin master command"})
        # 3. build with BASE_PATH/src/toHTML.py 
        os.chdir(settings.BASE_DIR)
        build_cmd = ("python src/cnExport.py -r %s -d %s -i" % (repo_path, build_path))
        try:
            subprocess.check_output(build_cmd.split())
        except Exception as e:
            os.chdir(settings.BASE_DIR)
            return JsonResponse({"success":"false", "reason":"error when running command"})
        
        # Normal conclusion
        os.chdir(settings.BASE_DIR)
        repo_object.last_compiled = datetime.datetime.now()
        repo_object.save()

    def post(self, request, slug, *args, **kwargs):
        self.build_repo(slug)
        return JsonResponse({"success":"true"})
        
    def get(self, request, slug, *args, **kwargs):
        self.build_repo(slug)
        return redirect(os.path.join(settings.STATIC_URL, slug, 'index.html'))


# FIXME : make simple template view for index.html of each static site 
#def visit_site(request, username, name):
#     return HttpResponse(u"Visiting site for repo user = %s | name = %s" % (username, name))
