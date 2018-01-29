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
    """
    home page
    """
    if request.user.is_authenticated:
        # if user is logged in
        return render(request,
                      'wikiserver/index.html',
                      {'username': request.user.username})
    else:
        return render(request, 'wikiserver/index.html')


def UserSignUpView(request):
    """
    user account creation form
    """
    if request.method == 'GET':
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('wikiserver:index', args=()))
        else:
            return render(request, 'wikiserver/signup.html')
    elif request.method == 'POST':
        # validate form
        if 'username' not in request.POST or 'password' not in request.POST or 'verify_password' not in request.POST:
            return render(request,
                          'wikiserver/signup.html',
                          {'error_message': "invalid form, did not contain username and/or password"},
                          status=400)

        u = request.POST['username']
        p = request.POST['password']
        vp = request.POST['verify_password']

        # validate, username is unique and alpha-numeric
        validation = CreateUserValidation.isValidUsername(u)
        if not validation['isValid']:
            return render(request,
                          'wikiserver/signup.html',
                          {'error_message': validation['message']},
                          status=400)

        # validate, password is at least 4 characters
        validation = CreateUserValidation.isValidPassword(p)
        if not validation['isValid']:
            return render(request,
                          'wikiserver/signup.html',
                          {
                            'error_message': validation['message'],
                            'username': u
                          },
                          status=400)

        # validate, passwords match
        if p != vp:
            return render(request,
                          'wikiserver/signup.html',
                          {
                            'error_message': 'Passwords do not match',
                            'username': u
                          },
                          status=400)

        # create user
        user = User.objects.create_user(u, None, p)
        user.save()

        # login user
        login(request, user)

        # redirect
        return HttpResponseRedirect(reverse('wikiserver:index', args=()))


def UserLogInView(request):
    """
    user log in form
    """
    if request.method == 'GET':
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('wikiserver:index', args=()))
        else:
            return render(request, 'wikiserver/login.html')
    elif request.method == 'POST':
        # validate form
        if 'username' not in request.POST or 'password' not in request.POST:
            return render(request,
                          'wikiserver/login.html',
                          {'error_message': "invalid form, did not contain username and/or password"},
                          status=400)

        u = request.POST['username']
        p = request.POST['password']

        # authenticate user
        user = authenticate(username=u, password=p)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('wikiserver:index', args=()))
        else:
            return render(request,
                          'wikiserver/login.html',
                          {'error_message': "invalid login, please try again"},
                          status=400)


def UserLogOut(request):
    """
    logs out user
    """
    logout(request)
    return HttpResponseRedirect(reverse('wikiserver:index', args=()))


def PageView(request, page_id):
    context = {'id':page_id}
    return render(request, 'wikiserver/page.html', context)
