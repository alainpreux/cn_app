#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import mimetypes
import os.path
import subprocess
import logging
import datetime

from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.views.generic import View

from .models import Repository

logger = logging.getLogger(__name__)
# Create your views here.


import shlex
#import logging
#import subprocess
from StringIO import StringIO

def run_shell_command(command_line):
    command_line_args = shlex.split(command_line)

    logger.warn('Subprocess: "' + command_line + '"')

    try:
        command_line_process = subprocess.Popen(
            command_line_args,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
        )

        process_output, _ =  command_line_process.communicate()

        # process_output is now a string, not a file,
        # you may want to do:
        # process_output = StringIO(process_output)
        #log_subprocess_output(process_output)
        logger.warn(process_output)
    except (OSError, CalledProcessError) as exception:
        logger.warn('Exception occured: ' + str(exception))
        logger.warn('Subprocess failed')
        return False
    else:
        # no exception was raised
        logger.warn('Subprocess finished')

    return True

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

    def build_repo(self, slug, request):
        # 1. cd to repo path
        repo_path = os.path.join(settings.REPOS_DIR, slug)
        build_path = os.path.join(settings.GENERATED_SITES_DIR, slug)
        base_url = request.build_absolute_uri(os.path.join(settings.STATIC_URL, settings.GENERATED_SITES_URL, slug))
        logger.warn("Post to buidl view ! repo_path = %s" % repo_path)
        logger.warn("+++ Base URL = %s" % base_url)

        repo_object = Repository.objects.all().filter(slug=slug)[0]
        try:
            os.chdir(repo_path)
        except Exception as e:
            return {"success":"false", "reason":"repo not existing, or not synced"}
        # 2. git pull origin [branch:'master']
        git_cmd1 = "git checkout %s " %  repo_object.default_branch
        git_cmd2 = "git pull origin %s" % repo_object.default_branch
        try:
            subprocess.check_output(git_cmd1.split())
            subprocess.check_output(git_cmd2.split())
        except Exception as e:
            os.chdir(settings.BASE_DIR)
            return {"success":"false", "reason":"error with git pull origin master command"}
        # 3. build with BASE_PATH/src/toHTML.py
        os.chdir(settings.BASE_DIR)
        build_cmd = ("python src/cnExport.py -r %s -d %s -u %s -i" % (repo_path, build_path, base_url))
        try:
            #subprocess.check_output(build_cmd.split())
			run_shell_command(build_cmd)
        except Exception as e:
            os.chdir(settings.BASE_DIR)
            return {"success":"false", "reason":"error when running command"}

        # Normal conclusion
        os.chdir(settings.BASE_DIR)
        repo_object.last_compiled = datetime.datetime.now()
        repo_object.save()
        return({"success":"true"})

    def post(self, request, slug, *args, **kwargs):
        res = self.build_repo(slug, request)
        return JsonResponse(res)

    def get(self, request, slug, *args, **kwargs):
        self.build_repo(slug, request)
        return redirect(reverse('visit_site', args=(slug,)))

def visit_site(request, slug):
    """ Just a redirection to static generated site """
    return redirect(os.path.join(settings.STATIC_URL, settings.GENERATED_SITES_URL, slug, 'index.html'))
