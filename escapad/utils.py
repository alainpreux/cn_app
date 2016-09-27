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


def cnrmtree(path):
    """ custom rmtree func to overcome unicode files bug """

    for root, dirs, files in os.walk(path.encode('utf-8'), topdown=False):
        for f in files:
        	os.remove(os.path.join(root, f).decode('utf-8'))
        for d in dirs:
        	os.rmdir(os.path.join(root, d).decode('utf-8'))
