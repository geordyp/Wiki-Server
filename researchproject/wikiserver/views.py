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

from .util import CreateUserValidation
from .models import Post


def IndexView(request):
    """
    home page
    """
    recentPosts = Post.objects.order_by('-pub_date')[:5]

    if request.user.is_authenticated:
        # if user is logged in
        return render(request,
                      'wikiserver/index.html',
                      {
                        'userLoggedIn': True,
                        'username': request.user.username,
                        'recentPosts': recentPosts
                      })
    else:
        return render(request,
                      'wikiserver/index.html',
                      {
                        'userLoggedIn': False,
                        'recentPosts': recentPosts
                      })


def UserSignUpView(request):
    """
    user account creation form
    """
    n = request.GET.get('next', None)   # next
    if request.method == 'POST':
        # validate form
        if 'username' not in request.POST or 'password' not in request.POST or 'verifyPassword' not in request.POST:
            return render(request,
                          'wikiserver/user-signup.html',
                          {
                            'userLoggedIn': False,
                            'n':n,
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
                            'n':n,
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
                            'n':n,
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
                            'n':n,
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
        if n is None: n = reverse('wikiserver:index', args=())
        return HttpResponseRedirect(n)
    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('wikiserver:index', args=()))

        return render(request,
                      'wikiserver/user-signup.html',
                      {'userLoggedIn': False,
                       'n': n})


def UserLogInView(request):
    """
    user log in form
    """
    n = request.GET.get('next', None)   # next
    if request.method == 'POST':
        # validate form
        if 'username' not in request.POST or 'password' not in request.POST:
            return render(request,
                          'wikiserver/user-login.html',
                          {
                            'userLoggedIn': False,
                            'n':n,
                            'errorMessage': "Invalid form, did not contain username and/or password"
                          },
                          status=400)

        u = request.POST['username']
        p = request.POST['password']

        # authenticate user
        user = authenticate(username=u, password=p)
        if user is not None:
            login(request, user)

            if n is None: n = reverse('wikiserver:index', args=())
            return HttpResponseRedirect(n)
        else:
            return render(request,
                          'wikiserver/user-login.html',
                          {
                            'userLoggedIn': False,
                            'n':n,
                            'errorMessage': "Invalid login, please try again"
                          },
                          status=400)
    else:
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('wikiserver:index', args=()))

        return render(request,
                      'wikiserver/user-login.html',
                      {'userLoggedIn': False,
                       'n': n})


def UserLogOut(request):
    """
    logs out user
    """
    logout(request)
    return HttpResponseRedirect(reverse('wikiserver:index', args=()))


@login_required
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

        post = Post(title=t, owner=request.user, content=c)
        post.save()

        return HttpResponseRedirect(reverse('wikiserver:post-view', args=(post.id,)))
    else:
        return render(request, 'wikiserver/post-create.html')


def PostView(request, postid):
    """
    view a post
    """
    try:
        p = Post.objects.get(id=postid)
        return render(request, 'wikiserver/post-view.html', {'post':p})
    except ObjectDoesNotExist:
        return HttpResponseRedirect(reverse('wikiserver:index', args=()))


def PostList(request, pageNum):
    """
    view a list of all posts, 5 per list-page
    """
    # get all posts
    allPosts = Post.objects.order_by('-pub_date')
    numOfPosts = len(allPosts)
    numOfPostsToDisplay = 10
    pageNum = int(pageNum)

    # get the number of list-pages
    numOfListPages = numOfPosts / numOfPostsToDisplay
    if numOfPosts % numOfPostsToDisplay != 0: numOfListPages+=1
    listPageNumbers = []
    for i in range(1, numOfListPages+1): listPageNumbers.append(i)

    # error check pageNum
    if pageNum < 1 or pageNum > numOfListPages:
        raise Http404("List-Page number does not exist")

    # get posts to display on this page
    start = (pageNum - 1) * numOfPostsToDisplay
    postsToDisplay = allPosts[start:start+numOfPostsToDisplay]

    # determine if there is a prev/next page
    hasPrev = False if pageNum == 1 else True
    hasNext = False if pageNum == numOfListPages else True

    return render(request,
                  'wikiserver/post-list.html',
                  {
                    'posts': postsToDisplay,
                    'hasPrev': hasPrev,
                    'hasNext': hasNext,
                    'curr': pageNum,
                    'prev': pageNum-1,
                    'next': pageNum+1,
                    'numOfPages': listPageNumbers
                  })
