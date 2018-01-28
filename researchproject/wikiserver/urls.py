from django.conf.urls import url

from . import views


app_name = 'wikiserver'
urlpatterns = [
    # ex: /wiki/
    url(r'^$', views.IndexView, name='index'),
    # ex: /wiki/signup/
    url(r'^signup/$', views.UserSignUpView, name='signup'),
    # ex: /wiki/login/
    url(r'^login/$', views.UserLogInView, name='login'),
    # ex: /wiki/logout/
    url(r'^logout/$', views.UserLogOut, name='logout'),
    # # ex: /wiki/5/
    url(r'^(?P<pk>[0-9]+)/$', views.PageView, name='page')
]
