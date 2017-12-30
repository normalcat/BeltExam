from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'main$', views.index),
    url(r'travels$',views.travels),
    url(r'travels/add$',views.add),
    url(r'travels/create$',views.create_trip),
    url(r'travels/join/(?P<tid>\d+)$',views.insert),
    url(r'users/login$',views.login),
    url(r'users/create$',views.create),
    url(r'users/success$',views.success),
    url(r'users/logout$',views.logout),
    url(r'travels/(?P<tid>\d+)$', views.destination),
]
