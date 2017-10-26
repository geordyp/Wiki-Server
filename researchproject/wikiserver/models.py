# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)

    def __str__(self):
        return self.name;


class Page(models.Model):
    title = models.CharField(max_length=300)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    pub_date = models.DateTimeField('date published')

    def __str__(self):
        return self.title;


class Post(models.Model):
    title = models.CharField(max_length=300)
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    content = models.TextField(max_length=1000)
    author = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title;
