from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^build/(?P<username>[\w-]+)/(?P<name>[\w-]+)/$', views.build_repo, name='build_repo'),
    url(r'^site/(?P<username>[\w-]+)/(?P<name>[\w-]+)/$', views.visit_site, name='visit_site'),
]