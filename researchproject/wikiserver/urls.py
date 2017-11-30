from django.conf.urls import url

from . import views


app_name = 'wikiserver'
urlpatterns = [
    # ex: /wiki/
    url(r'^$', views.IndexView, name='index'),
    # ex: /wiki/signup/
    url(r'^signup/$', views.SignUpView, name='signup'),
    # ex: /wiki/5/
    url(r'^(?P<pk>[0-9]+)/$', views.PageView, name='page'),

    url(r'^createuseraccount/$', views.CreateUserAccount, name='createuseraccount'),
]
