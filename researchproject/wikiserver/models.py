# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# class Page(models.Model):
#     title = models.CharField(max_length=300, null=False, blank=False, unique=True)
#     owner = models.ForeignKey(UserAccount, on_delete=models.CASCADE, null=False, blank=False)
#     content = models.TextField(max_length=1000)
#     pub_date = models.DateTimeField('date published')
#
#     def __str__(self):
#         return self.title;
