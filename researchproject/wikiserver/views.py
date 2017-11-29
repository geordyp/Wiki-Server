# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render


def home(request):
    context = {'name':'geordy williams'}
    return render(request, 'wikiserver/home.html', context)


def page(request, page_id):
    context = {'id':page_id}
    return render(request, 'wikiserver/page.html', context)
