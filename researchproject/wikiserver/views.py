# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.views import generic
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required

from .util import CreateUserValidation, FormValidation
from .models import Page


def IndexView(request):
    """
    home page
    """

    state = {
        'username': request.user.username,
        'recentPages': Page.objects.order_by('-pub_date')[:5]
    }

    return render(request, 'wikiserver/index.html', state)


def UserJoinView(request):
    """
    user account creation form
    """

    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('wikiserver:index', args=()))

    state = {
        'username': None,
        'next': request.GET.get('next', None),
        'errorMessage': None,
        'formUsername': ''
    }

    if request.method == 'POST':
        # validate form
        fields = ['username', 'password', 'verifyPassword']
        if not FormValidation.formContainsAll(request.POST, fields):
            state['errorMessage'] = 'Invalid form, did not contain username, password, and/or verifyPassword'
            return render(request, 'wikiserver/user-join.html', state, status=400)

        uInput = state['formUsername'] = str(request.POST['username'])
        pInput = str(request.POST['password'])
        vpInput = str(request.POST['verifyPassword'])

        # validate, username is unique and alpha-numeric
        validation = CreateUserValidation.isValidUsername(uInput)
        if not validation['isValid']:
            state['errorMessage'] = validation['message']
            state['formUsername'] = ''
            return render(request, 'wikiserver/user-join.html', state, status=400)

        # validate, password is at least 4 characters
        validation = CreateUserValidation.isValidPassword(pInput)
        if not validation['isValid']:
            state['errorMessage'] = validation['message']
            return render(request, 'wikiserver/user-join.html', state, status=400)

        # validate, passwords match
        if pInput != vpInput:
            state['errorMessage'] = 'Passwords do not match'
            return render(request, 'wikiserver/user-join.html', state, status=400)

        # create user
        user = User.objects.create_user(uInput, None, pInput)
        user.save()

        # login user
        login(request, user)

        # redirect
        if state['next'] is None:
            state['next'] = reverse('wikiserver:index', args=())

        return HttpResponseRedirect(state['next'])

    else:
        return render(request, 'wikiserver/user-join.html', state)


def UserLogInView(request):
    """
    user log in form
    """

    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('wikiserver:index', args=()))

    state = {
        'username': None,
        'next': request.GET.get('next', None),
        'errorMessage': None
    }

    if request.method == 'POST':
        # validate form
        fields = ['username', 'password']
        if not FormValidation.formContainsAll(request.POST, fields):
            state['errorMessage'] = 'Invalid form, did not contain username and/or password'
            return render(request, 'wikiserver/user-login.html', state, status=400)

        uInput = str(request.POST['username'])
        pInput = str(request.POST['password'])

        # authenticate user
        user = authenticate(username=uInput, password=pInput)
        if user is None:
            state['errorMessage'] = 'Invalid login, please try again'
            return render(request, 'wikiserver/user-login.html', state, status=400)
        else:
            login(request, user)
            if state['next'] is None:
                state['next'] = reverse('wikiserver:index', args=())

            return HttpResponseRedirect(state['next'])

    else:
        return render(request, 'wikiserver/user-login.html', state)


def UserLogOut(request):
    """
    logs out user
    """

    logout(request)
    return HttpResponseRedirect(reverse('wikiserver:index', args=()))


@login_required
def PageCreate(request):
    """
    page creation form
    """

    state = {
        'username': request.user.username,
        'errorMessage': None,
        'formTitle': '',
        'formContent': ''
    }

    if request.method == 'POST':
        # validate form
        fields = ['title', 'content']
        if not FormValidation.formContainsAll(request.POST, fields):
            state['errorMessage'] = 'Invalid form, did not contain title and/or content'
            return render(request, 'wikiserver/user-join.html', state, status=400)

        tInput = state['formTitle'] = request.POST['title']
        cInput = state['formContent'] = request.POST['content']

        # validate title
        if len(tInput) < 1:
            state['errorMessage'] = "Please provide a title"
            return render(request, 'wikiserver/page-create.html', state, status=400)

        # validate content
        if len(cInput) < 1:
            state['errorMessage'] = "Page must have content"
            return render(request, 'wikiserver/page-create.html', state, status=400)

        page = Page(title=tInput, owner=request.user, content=cInput)
        page.save()

        return HttpResponseRedirect(reverse('wikiserver:page-view', args=(page.id,)))

    else:
        return render(request, 'wikiserver/page-create.html', state)


def PageView(request, pageid):
    """
    view a page
    """

    state = {
        'username': request.user.username,
        'page': {}
    }

    try:
        state['page'] = Page.objects.get(id=pageid)
    except Page.DoesNotExist:
        raise Http404("Page does not exist")

    return render(request, 'wikiserver/page-view.html', state)


def PageList(request, chapter):
    """
    view a list of all pages, 10 per chapter
    chapter is equivalent to list-page
    """

    state = {
        'username': request.user.username,
        'pagesToDisplay': [],
        'chapterLinks': []
    }

    # get all pages
    allPages = Page.objects.order_by('-pub_date')
    numOfPages = len(allPages)

    # number of pages to display per list-page
    chapterSize = 10

    # get the total number of chapters
    numOfChapters = numOfPages / chapterSize
    if numOfPages % chapterSize != 0:
        numOfChapters += 1

    # error check current chapter
    chapter = curr = int(chapter)
    if chapter < 1:
        return HttpResponseRedirect(reverse('wikiserver:page-list', args=(1,)))
    elif chapter > numOfChapters:
        return HttpResponseRedirect(reverse('wikiserver:page-list', args=(numOfChapters,)))

    # get pages to display
    start = (chapter - 1) * chapterSize
    state['pagesToDisplay'] = allPages[start : start + chapterSize]

    # if has previous
    if curr > 1:
        state['chapterLinks'].append({'link': curr - 1, 'text': 'prev'})

    # get the full list of chapters
    for i in range(1, numOfChapters + 1):
        state['chapterLinks'].append({'link': i, 'text': i})

    # if has next
    if curr < numOfChapters:
        state['chapterLinks'].append({'link': curr + 1, 'text': 'next'})

    return render(request, 'wikiserver/page-list.html', state)
