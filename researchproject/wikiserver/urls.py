from django.conf.urls import url

from . import views


app_name = 'wikiserver'
urlpatterns = [
    # ex: /wiki/
    url(r'^$', views.IndexView, name='index'),

    # ex: /wiki/user/join/
    url(r'^user/join/$', views.UserJoinView, name='user-join'),
    # ex: /wiki/user/login/
    url(r'^user/login/$', views.UserLogInView, name='user-login'),
    # ex: /wiki/user/logout/
    url(r'^user/logout/$', views.UserLogOut, name='user-logout'),

    # ex: /wiki/post/create/
    url(r'^post/create/$', views.PostCreate, name='post-create'),
    # ex: /wiki/post/1/
    url(r'^post/(?P<postid>[0-9]+)/$', views.PostView, name='post-view'),
    # ex: /wiki/post/list/1/
    url(r'^post/list/(?P<pageNum>[0-9]+)/$', views.PostList, name='post-list')
]
