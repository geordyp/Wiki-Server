from django.conf.urls import url

from . import views


urlpatterns = [
    # ex: /wiki/
    url(r'^$', views.home, name='home'),
    # ex: /wiki/5/
    url(r'^(?P<page_id>[0-9]+)/$', views.page, name='page')
    # ex: /wiki/users/geordyp/
    # url(r'^(?P<page_id>[0-9]+)/$', views.page, name='user')
]
