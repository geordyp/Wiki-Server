# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from .models import UserAccount


def IndexView(request):
    context = {'name':'geordy williams'}
    return render(request, 'wikiserver/index.html', context)


def SignUpView(request):
    return render(request, 'wikiserver/signup.html')


def CreateUserAccount(request):
    # validate input TODO further validation
    if 'username' not in request.POST or request.POST['username'] == '':
        return render(request, 'wikiserver/signup.html', {
            'error_message': "invalid username",
        }, status=400)
    if 'password' not in request.POST or request.POST['password'] == '':
        return render(request, 'wikiserver/signup.html', {
            'error_message': "invalid password",
        }, status=400)

    # create user TODO hash password
    ua = UserAccount(username=request.POST['username'], password=request.POST['password'])
    ua.save();

    # redirect
    return HttpResponseRedirect(reverse('wikiserver:index', args=()))


def PageView(request, page_id):
    context = {'id':page_id}
    return render(request, 'wikiserver/page.html', context)
