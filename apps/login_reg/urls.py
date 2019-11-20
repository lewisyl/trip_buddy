from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^registering$', views.registering),
    url(r'^logging_in$', views.logging_in),
]