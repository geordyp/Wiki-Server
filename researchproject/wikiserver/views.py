# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic

from .models import UserAccount

from .util import UserAccountValidation
from .util import UserAccountPWHash


def IndexView(request):
    context = {'name':'geordy williams'}
    return render(request, 'wikiserver/index.html', context)


def SignUpView(request):
    return render(request, 'wikiserver/signup.html')


def CreateUserAccount(request):
    # validate form
    if 'username' not in request.POST or 'password' not in request.POST:
        return render(request, 'wikiserver/signup.html', {
            'error_message': "invalid form, did not contain username and/or password",
        }, status=400)

    # validate, username is unique and alpha-numeric
    validation = UserAccountValidation.isValidUsername(request.POST['username'])
    if not validation['isValid']:
        return render(request, 'wikiserver/signup.html', {
            'error_message': validation['message'],
        }, status=400)

    # validate, password is at least 4 characters
    validation = UserAccountValidation.isValidPassword(request.POST['password'])
    if not validation['isValid']:
        return render(request, 'wikiserver/signup.html', {
            'error_message': validation['message'],
        }, status=400)

    # create user
    # password_hash = UserAccountPWHash.make_pw_hash(request.POST['password'])
    ua = UserAccount(username=request.POST['username'], pw_hash=request.POST['password'])
    ua.save()

    # redirect
    return HttpResponseRedirect(reverse('wikiserver:index', args=()))


def PageView(request, page_id):
    context = {'id':page_id}
    return render(request, 'wikiserver/page.html', context)
