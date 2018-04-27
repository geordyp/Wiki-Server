# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class Page(models.Model):
    version = models.IntegerField(default=1, null=False, blank=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=300, default='title unavailable', null=False, blank=True)
    content = models.TextField(max_length=40000, default='content unavailable', null=False, blank=True)
    pub_date = models.DateTimeField('date published', auto_now_add=True, null=True)

    def __str__(self):
        return "%s BY %s" % self.title, self.owner.username;
