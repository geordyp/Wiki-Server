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
        'username': None,
        'recentPages': Page.objects.order_by('-pub_date')[:5]
    }

    if request.user.is_authenticated:
        state['username'] = request.user.username

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
    try:
        p = Page.objects.get(id=pageid)
        return render(request, 'wikiserver/page-view.html', {'page':p})
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('wikiserver:index', args=()))


def PageList(request, listGroupNum):
    """
    view a list of all pages, 5 per list-page
    """
    # get all pages
    allPages = Page.objects.order_by('-pub_date')
    numOfPages = len(allPages)
    numOfPagesToDisplay = 10
    listGroupNum = int(listGroupNum)

    # get the number of list groups
    numOfListGroups = numOfPages / numOfPagesToDisplay
    if numOfPages % numOfPagesToDisplay != 0: numOfListGroups+=1
    listGroupNumbers = []
    for i in range(1, numOfListGroups+1): listGroupNumbers.append(i)

    # error check listGroupNum
    if listGroupNum < 1 or listGroupNum > numOfListGroups:
        raise Http404("List-page number does not exist")

    # get pages to display
    start = (listGroupNum - 1) * numOfPagesToDisplay
    pagesToDisplay = allPages[start:start+numOfPagesToDisplay]

    # determine if there is a prev/next page
    hasPrev = False if listGroupNum == 1 else True
    hasNext = False if listGroupNum == numOfListGroups else True

    return render(request,
                  'wikiserver/page-list.html',
                  {
                    'pages': pagesToDisplay,
                    'hasPrev': hasPrev,
                    'hasNext': hasNext,
                    'curr': listGroupNum,
                    'prev': listGroupNum-1,
                    'next': listGroupNum+1,
                    'numOfListGroups': listGroupNumbers
                  })
