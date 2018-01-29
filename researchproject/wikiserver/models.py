# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User


class Post(models.Model):
    title = models.CharField(max_length=300, null=False, blank=False, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False)
    content = models.TextField(max_length=1000)
    pub_date = models.DateTimeField('date published', auto_now_add=True)

    def __str__(self):
        return self.title;
