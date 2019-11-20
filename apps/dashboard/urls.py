from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.dashboard),
    url(r'^logout$', views.logout),
    url(r'^add_trip$', views.add_trip),
    url(r'^add_trip_process$', views.add_trip_process),
    url(r'^(?P<trip_id>\d+)$', views.detail),
    url(r'^(?P<trip_id>\d+)/join$', views.join),
    url(r'^(?P<trip_id>\d+)/cancel$', views.cancel),
    url(r'^(?P<trip_id>\d+)/edit_trip$', views.edit_trip),
    url(r'^(?P<trip_id>\d+)/edit_trip_process$', views.edit_trip_process),
    url(r'^(?P<trip_id>\d+)/remove_trip$', views.remove)
]