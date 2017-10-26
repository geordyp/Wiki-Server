# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello, world. You're at the wiki index.")


def page(request, page_id):
    return HttpResponse("You're looking at page %s." % page_id)
