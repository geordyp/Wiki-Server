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
                      {
                        'userLoggedIn': True,
                        'username': request.user.username
                      })
    else:
        return render(request,
                      'wikiserver/index.html',
                      {'userLoggedIn': False})


def UserSignUpView(request):
    """
    user account creation form
    """
    if request.method == 'POST':
        # validate form
        if 'username' not in request.POST or 'password' not in request.POST or 'verifyPassword' not in request.POST:
            return render(request,
                          'wikiserver/user-signup.html',
                          {
                            'userLoggedIn': False,
                            'errorMessage': "Invalid form, did not contain username and/or password"
                          },
                          status=400)

        u = request.POST['username']
        p = request.POST['password']
        vp = request.POST['verifyPassword']

        # validate, username is unique and alpha-numeric
        validation = CreateUserValidation.isValidUsername(u)
        if not validation['isValid']:
            return render(request,
                          'wikiserver/user-signup.html',
                          {
                            'userLoggedIn': False,
                            'errorMessage': validation['message']
                          },
                          status=400)

        # validate, password is at least 4 characters
        validation = CreateUserValidation.isValidPassword(p)
        if not validation['isValid']:
            return render(request,
                          'wikiserver/user-signup.html',
                          {
                            'userLoggedIn': False,
                            'errorMessage': validation['message'],
                            'username': u
                          },
                          status=400)

        # validate, passwords match
        if p != vp:
            return render(request,
                          'wikiserver/user-signup.html',
                          {
                            'userLoggedIn': False,
                            'errorMessage': 'Passwords do not match',
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
    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('wikiserver:index', args=()))
        else:
            return render(request,
                          'wikiserver/user-signup.html',
                          {'userLoggedIn': False})


def UserLogInView(request):
    """
    user log in form
    """
    if request.method == 'POST':
        # validate form
        if 'username' not in request.POST or 'password' not in request.POST:
            return render(request,
                          'wikiserver/user-login.html',
                          {
                            'userLoggedIn': False,
                            'errorMessage': "Invalid form, did not contain username and/or password"
                          },
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
                          'wikiserver/user-login.html',
                          {
                            'userLoggedIn': False,
                            'errorMessage': "Invalid login, please try again"
                          },
                          status=400)
    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('wikiserver:index', args=()))
        else:
            return render(request,
                          'wikiserver/user-login.html',
                          {'userLoggedIn': False})


def UserLogOut(request):
    """
    logs out user
    """
    logout(request)
    return HttpResponseRedirect(reverse('wikiserver:index', args=()))


def PostCreate(request):
    """
    post creation form
    """
    if request.method == 'POST':
        # validate form
        if 'title' not in request.POST or 'content' not in request.POST:
            return render(request,
                          'wikiserver/post-create.html',
                          {
                            'userLoggedIn': True,
                            'errorMessage': "Invalid form, did not contain title and/or content"
                          },
                          status=400)

        t = request.POST['title']
        c = request.POST['content']

        # validate title
        if len(t) < 1:
            return render(request,
                          'wikiserver/post-create.html',
                          {
                            'userLoggedIn': True,
                            'errorMessage': "Please provide a title"
                          },
                          status=400)
        # validate content
        if len(c) < 1:
            return render(request,
                          'wikiserver/post-create.html',
                          {
                            'userLoggedIn': True,
                            'errorMessage': "Post must have content"
                          },
                          status=400)

        # make sure user is logged in
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse('wikiserver:user-login', args=()))

        post = Post(title=t, owner=request.user.username, content=c)
        post.save()

        return HttpResponseRedirect(reverse('wikiserver:post-view', args=(post.id)))
    else:
        if request.user.is_authenticated:
            return render(request, 'wikiserver/post-create.html')
        else:
            return HttpResponseRedirect(reverse('wikiserver:user-login', args=()))


def PostView(request, postid):
    return render(request, 'wikiserver/post-view.html', {'id':postid})
