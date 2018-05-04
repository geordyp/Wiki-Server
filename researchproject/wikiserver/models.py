# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class Page(models.Model):
    """
    contains current page info
    """
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    title = models.CharField(max_length=300, default='title unavailable', null=False, blank=True)
    content = models.TextField(max_length=40000, default='content unavailable', null=False, blank=True)
    date_edited = models.DateTimeField(auto_now=True, null=True)


class Page_Version(models.Model):
    """
    contains previous page info for version control
    """
    page = models.ForeignKey(Page, on_delete=models.CASCADE, null=True)
    version = models.IntegerField(default=1, null=True)
    title = models.CharField(max_length=300, default='title unavailable', null=False, blank=True)
    content = models.TextField(max_length=40000, default='content unavailable', null=False, blank=True)
    date_edited = models.DateTimeField(auto_now_add=True, null=True)
