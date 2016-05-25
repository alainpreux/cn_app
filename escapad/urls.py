from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^build/(?P<slug>[\w-]+)/$', views.BuildView.as_view(), name='build_repo'),
    #FIXME make a template view ? url(r'^site/(?P<username>[\w-]+)/(?P<name>[\w-]+)/$', views.visit_site, name='visit_site'),
]