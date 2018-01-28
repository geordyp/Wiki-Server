# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login

from .util import CreateUserValidation


def IndexView(request):
    if request.user.is_authenticated:
        return render(request, 'wikiserver/index.html', {'username': request.user.username})
    else:
        return render(request, 'wikiserver/index.html')


def UserSignUpView(request):
    if request.method == 'GET':
        return render(request, 'wikiserver/signup.html')
    elif request.method == 'POST':
        # validate form
        if 'username' not in request.POST or 'password' not in request.POST or 'verify_password' not in request.POST:
            return render(request, 'wikiserver/signup.html', {
                'error_message': "invalid form, did not contain username and/or password",
            }, status=400)

        # validate, username is unique and alpha-numeric
        validation = CreateUserValidation.isValidUsername(request.POST['username'])
        if not validation['isValid']:
            return render(request, 'wikiserver/signup.html', {
                'error_message': validation['message'],
            }, status=400)

        # validate, password is at least 4 characters
        validation = CreateUserValidation.isValidPassword(request.POST['password'])
        if not validation['isValid']:
            return render(request, 'wikiserver/signup.html', {
                'error_message': validation['message'],
                'username': request.POST['username'],
            }, status=400)

        # validate, passwords match
        if request.POST['password'] != request.POST['verify_password']:
            return render(request, 'wikiserver/signup.html', {
                'error_message': 'Passwords do not match',
                'username': request.POST['username'],
            }, status=400)

        # create user
        user = User.objects.create_user(request.POST['username'], None, request.POST['password'])
        user.save()

        # login user
        login(request, user)

        # redirect
        return HttpResponseRedirect(reverse('wikiserver:index', args=()))


def PageView(request, page_id):
    context = {'id':page_id}
    return render(request, 'wikiserver/page.html', context)
