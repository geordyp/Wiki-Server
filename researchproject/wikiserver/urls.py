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

    # ex: /wiki/page/create/
    url(r'^page/create/$', views.PageCreate, name='page-create'),
    # ex: /wiki/page/1/
    url(r'^page/(?P<pageid>[0-9]+)/$', views.PageView, name='page-view'),
    # ex: /wiki/page/list/1/
    url(r'^page/list/(?P<listGroupNum>[0-9]+)/$', views.PageList, name='page-list')
]
