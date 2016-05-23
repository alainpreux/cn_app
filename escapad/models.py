#!/usr/bin/python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

import os
import subprocess

from django.conf import settings
from django.db import models
from django.core.exceptions import ValidationError

# Create your models here.

class Repository(models.Model):
    
        
    def set_name(self, url):
        try:
            name = url.strip('/').rsplit('/',1)[-1].strip('.git').lower()
        except Exception as e:
            name = "default_name"
        return name
    
    def set_user(self, url):
        try:
            user = url.strip('/').rsplit('/', 2)[-2].lower()
        except Exception as e:
            user = "default_user"
        return user
    
    def set_provider(self, url):
        try:
            provider = url.strip('/').rsplit('/', 3)[-3].lower()
        except Exception as e:
            provider = "http://github.com"
        return provider
    
    def save(self, *args, **kwargs):
        """ populate some fields from git url and create directory before saving"""
        if not self.git_name:
            self.git_name = self.set_name(self.git_url)
        if not self.git_username:
            self.git_username = self.set_user(self.git_url)
        if not self.provider:
            self.provider = self.set_provider(self.git_url)
        super(Repository, self).save(*args, **kwargs)

    git_url = models.URLField(max_length=200, unique=True)
    git_name = models.CharField(max_length=200, blank=True, null=True)
    git_username = models.CharField(max_length=200, blank=True, null=True)
    last_compiled = models.DateTimeField(blank=True, null=True)
    repo_synced = models.BooleanField(default=False)
    provider = models.URLField(max_length=200, blank=True, null=True)

    class Meta:
        unique_together = ('git_name', 'git_username')
    
