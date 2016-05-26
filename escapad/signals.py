#!/usr/bin/python
# -*- coding: utf-8 -*-

#from io import open
import json
import logging
import os
import subprocess
from django.utils import timezone

from django.conf import settings

from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
# from django.utils import datetime
from escapad.models import Repository

logger = logging.getLogger(__name__) # see in cn_app.settings.py logger declaration

@receiver(post_save, sender=Repository)
def create_repo_dir(sender, instance, created, update_fields, **kwargs):
    """ Create a dir repo_user/repo_name with clone of repo_url """
    logger.warning(" %s | creating repo dir ! create = %s, update_fields = %s" % (timezone.now(), created, update_fields))
    if update_fields == {'repo_synced'}:
        return
    if created:
        repo_path = os.path.join(settings.REPOS_DIR, instance.slug)
        current_path = os.path.abspath(os.getcwd())
        try:
            if not os.path.isdir(repo_path):
                os.makedirs(repo_path)
            os.chdir(repo_path)
            git_cmd = ("git clone %s ." % instance.git_url)
            subprocess.check_output(git_cmd.split())
            
        except Exception as e:
            logger.error("Problem when creating dir %s with url %s \n Error : %s " % ( instance.slug, instance.git_url, e))
            os.chdir(current_path)
            return False
        # In any case, go back to current_path
        os.chdir(current_path)
        logger.warning(" successful creation of repo %s with url %s" % (instance.slug, instance.git_url))
        instance.repo_synced = True
        instance.save(update_fields={'repo_synced'})
        return
    else:
        return

@receiver(post_delete, sender=Repository)
def delete_repo_dir(sender, instance, **kwargs):
    pass