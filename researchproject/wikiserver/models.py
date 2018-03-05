# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(max_length=300, null=True, blank=False)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=False)
    content = models.TextField(max_length=40000, default='no content', null=True)
    pub_date = models.DateTimeField('date published', auto_now_add=True, null=True)

    def __str__(self):
        return self.title;
