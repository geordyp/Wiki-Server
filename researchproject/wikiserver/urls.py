from django.conf.urls import url

from . import views


urlpatterns = [
    # ex: /wiki/
    url(r'^$', views.index, name='index'),
    # ex: /wiki/5/
    url(r'^(?P<page_id>[0-9]+)/$', views.page, name='page')
]
