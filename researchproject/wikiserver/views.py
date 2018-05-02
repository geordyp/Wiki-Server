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

from .util import CreateUserValidation, FormValidation, PageUtil
from .models import Page, Page_Version
import requests


def IndexView(request):
    """
    home page
    """

    context = {
        'username': request.user.username,
        'recentPages': []
    }

    pages = reversed(Page.objects.order_by('-date_created')[:5])
    # get latest versions
    for p in pages:
        context['recentPages'].append(PageUtil.getLatestVersion(p.id))

    return render(request, 'wikiserver/index.html', context)


def UserJoinView(request):
    """
    user account creation form
    """

    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('wikiserver:index', args=()))

    context = {
        'username': None,
        'next': request.GET.get('next', None),
        'errorMessage': None,
        'formUsername': ''
    }

    if request.method == 'POST':
        # validate form
        fields = ['username', 'password', 'verifyPassword']
        if not FormValidation.formContainsAll(request.POST, fields):
            context['errorMessage'] = 'Invalid form, did not contain username, password, and/or verifyPassword'
            return render(request, 'wikiserver/user-join.html', context, status=400)

        uInput = context['formUsername'] = str(request.POST['username'])
        pInput = str(request.POST['password'])
        vpInput = str(request.POST['verifyPassword'])

        # validate, username is unique and alpha-numeric
        validation = CreateUserValidation.isValidUsername(uInput)
        if not validation['isValid']:
            context['errorMessage'] = validation['message']
            context['formUsername'] = ''
            return render(request, 'wikiserver/user-join.html', context, status=400)

        # validate, password is at least 4 characters
        validation = CreateUserValidation.isValidPassword(pInput)
        if not validation['isValid']:
            context['errorMessage'] = validation['message']
            return render(request, 'wikiserver/user-join.html', context, status=400)

        # validate, passwords match
        if pInput != vpInput:
            context['errorMessage'] = 'Passwords do not match'
            return render(request, 'wikiserver/user-join.html', context, status=400)

        # create user
        user = User.objects.create_user(uInput, None, pInput)
        user.save()

        # login user
        login(request, user)

        # redirect
        if context['next'] is None:
            context['next'] = reverse('wikiserver:index', args=())

        return HttpResponseRedirect(context['next'])

    else:
        return render(request, 'wikiserver/user-join.html', context)


def UserLogInView(request):
    """
    user log in form
    """

    if request.user.is_authenticated:
        return HttpResponseRedirect(reverse('wikiserver:index', args=()))

    context = {
        'username': None,
        'next': request.GET.get('next', None),
        'errorMessage': None
    }

    if request.method == 'POST':
        # validate form
        fields = ['username', 'password']
        if not FormValidation.formContainsAll(request.POST, fields):
            context['errorMessage'] = 'Invalid form, did not contain username and/or password'
            return render(request, 'wikiserver/user-login.html', context, status=400)

        uInput = str(request.POST['username'])
        pInput = str(request.POST['password'])

        # authenticate user
        user = authenticate(username=uInput, password=pInput)
        if user is None:
            context['errorMessage'] = 'Invalid login, please try again'
            return render(request, 'wikiserver/user-login.html', context, status=400)
        else:
            login(request, user)
            if context['next'] is None:
                context['next'] = reverse('wikiserver:index', args=())

            return HttpResponseRedirect(context['next'])

    else:
        return render(request, 'wikiserver/user-login.html', context)


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

    context = {
        'username': request.user.username,
        'creatingNewPage': True,
        'formTitle': '',
        'formContent': '',
        'errorMessage': None,
        'disable': False
    }

    if request.method == 'POST':
        # validate form
        fields = ['title', 'content']
        if not FormValidation.formContainsAll(request.POST, fields):
            context['errorMessage'] = 'Invalid form, did not contain title and/or content'
            return render(request, 'wikiserver/page-editor.html', context, status=400)

        tInput = context['formTitle'] = request.POST['title']
        cInput = context['formContent'] = request.POST['content']

        # validate title
        if len(tInput) < 1:
            context['errorMessage'] = "Please provide a title"
            return render(request, 'wikiserver/page-editor.html', context, status=400)

        # validate content
        if len(cInput) < 1:
            context['errorMessage'] = "Page must have content"
            return render(request, 'wikiserver/page-editor.html', context, status=400)

        page = Page(title=tInput, owner=request.user, content=cInput)
        page.save()

        return HttpResponseRedirect(reverse('wikiserver:page-view', args=(page.id,)))

    else:
        return render(request, 'wikiserver/page-editor.html', context)


def PageView(request, pageid):
    """
    view a page
    """

    context = {
        'username': request.user.username,
        'page': {},
        'markdownAvailable': True
    }

    context['page'] = PageUtil.getLatestVersion(pageid)
    if context['page'] == None:
        raise Http404("Page does not exist")

    try:
        headers = {'Content-Type': 'text/plain'}
        data = context['page'].content
        md = requests.post('https://api.github.com/markdown/raw', headers=headers, data=data)
        if md.status_code < 300:
            context['page'].content = md.text
        else:
            context['markdownAvailable'] = False
            print('%d error: %s' % (md.status_code, md.text,))
    except requests.exceptions.RequestException as e:
        context['markdownAvailable'] = False
        print('error: %s' % (e,))

    return render(request, 'wikiserver/page-view.html', context)


@login_required
def PageEdit(request, pageid):
    """
    page edit form
    """

    context = {
        'username': request.user.username,
        'creatingNewPage': False,
        'pid': pageid,
        'formTitle': '',
        'formContent': '',
        'errorMessage': None,
        'disable': False
    }

    try:
        page = Page.objects.get(id=pageid)
        if (page.owner != request.user):
            context['formTitle'] = page.title
            context['formContent'] = page.content
            context['errorMessage'] = 'Only the author can edit this page.'
            context['disable'] = True
            return render(request, 'wikiserver/page-editor.html', context, status=403)
    except Page.DoesNotExist:
        raise Http404("Page does not exist")

    if request.method == 'POST':
        # validate form
        fields = ['title', 'content']
        if not FormValidation.formContainsAll(request.POST, fields):
            context['errorMessage'] = 'Invalid form, did not contain title and/or content'
            return render(request, 'wikiserver/page-editor.html', context, status=400)

        tInput = context['formTitle'] = request.POST['title']
        cInput = context['formContent'] = request.POST['content']

        # validate title
        if len(tInput) < 1:
            context['errorMessage'] = "Please provide a title"
            return render(request, 'wikiserver/page-editor.html', context, status=400)

        # validate content
        if len(cInput) < 1:
            context['errorMessage'] = "Page must have content"
            return render(request, 'wikiserver/page-editor.html', context, status=400)

        page.title = tInput
        page.content = cInput
        page.save()

        return HttpResponseRedirect(reverse('wikiserver:page-view', args=(page.id,)))

    else:
        context['formTitle'] = page.title
        context['formContent'] = page.content
        return render(request, 'wikiserver/page-editor.html', context)


def PageList(request, chapter):
    """
    view a list of all pages, 10 per chapter
    chapter is equivalent to list-page
    """

    context = {
        'username': request.user.username,
        'pagesToDisplay': [],
        'chapterLinks': []
    }

    # get all pages
    allPages = Page.objects.order_by('-pub_date')
    numOfPages = len(allPages)

    # number of pages to display per chapter (list-page)
    chapterSize = 2

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
    context['pagesToDisplay'] = allPages[start : start + chapterSize]

    # if has previous
    if curr > 1:
        context['chapterLinks'].append({'link': curr - 1, 'text': 'prev'})

    # get the full list of chapters
    for i in range(1, numOfChapters + 1):
        context['chapterLinks'].append({'link': i, 'text': i})

    # if has next
    if curr < numOfChapters:
        context['chapterLinks'].append({'link': curr + 1, 'text': 'next'})

    return render(request, 'wikiserver/page-list.html', context)
