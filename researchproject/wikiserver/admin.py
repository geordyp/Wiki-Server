# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from .models import User, Page

# Register your models here.

admin.site.register(User)
admin.site.register(Page)
