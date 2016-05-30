#!/usr/bin/python
# -*- coding: utf-8 -*-
import json
import logging
import os
import subprocess
import shutil

from django.utils import timezone
from django.conf import settings
from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver

from escapad.models import Repository

logger = logging.getLogger(__name__) # see in cn_app.settings.py logger declaration

def create_repo_dir(dir_name, repo_url):
    """ function to create and sync a git repo(repo_url) with local dir (dir_name) """
    repo_path = os.path.join(settings.REPOS_DIR, dir_name)
    current_path = os.path.abspath(os.getcwd())
    try:
        if not os.path.isdir(repo_path):
            os.makedirs(repo_path)
        else:
            shutil.rmtree(repo_path)
            os.makedirs(repo_path)
        os.chdir(repo_path)
        git_cmd = ("git clone %s ." % repo_url)
        subprocess.check_output(git_cmd.split())    
    except Exception as e:
        logger.error("Problem when creating and syncing dir %s with url %s \n Error : %s " % ( dir_name, repo_url, e))
        os.chdir(current_path)
        return False
    # In any case, go back to current_path
    os.chdir(current_path)
    logger.warning(" successful creation of repo %s with url %s" % (dir_name, repo_url))
    return True


@receiver(post_delete, sender=Repository)
def delete_repo_dir(instance, **kwargs):
    """ utility function to delete repo dir 
    FIXME : and generated sites also!"""
    repo_path = os.path.join(settings.REPOS_DIR, instance.slug)
    try:
        shutil.rmtree(repo_path)
    except Exception as e:
        logger.error("Problem when deleting repo dir %s" %  repo_path)
    sites_path = os.path.join(settings.GENERATED_SITES_DIR, instance.slug)
    try:
        shutil.rmtree(sites_path)
    except Exception as e:
        logger.error("Problem when deleting sites dir %s" %  sites_path)
    return True


@receiver(pre_save, sender=Repository)
def resync_repo_dir(sender, instance, update_fields, **kwargs):
    """ when updating a Repo, resync dir if url has changed """
    # check if being updated
    if instance.id:
        old_repo = Repository.objects.get(pk=instance.id)
        # if git_url changed, delete old dir and create new one
        if instance.git_url != old_repo.git_url:
            delete_repo_dir(old_repo)
            slug = Repository.set_slug(instance.git_url)
            create_repo_dir(slug, instance.git_url)
            return
        # FIXME if default branch changed resync it!

@receiver(post_save, sender=Repository)
def sync_repo_dir(sender, instance, created, update_fields, **kwargs):
    """ Create a dir repo_user/repo_name with clone of repo_url """
    logger.warning(" %s | creating repo dir ! create = %s, update_fields = %s" % (timezone.now(), created, update_fields))
    if update_fields == {'repo_synced'}:
        return
    if created: #new record
        instance.repo_synced = create_repo_dir(instance.slug, instance.git_url)
        instance.save(update_fields={'repo_synced'})
        return
    else: # updating a repo object => see above pre_save receiver
        return
