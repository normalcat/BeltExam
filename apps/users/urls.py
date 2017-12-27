from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'main$', views.index),
    url(r'pokes$',views.pokes),
    url(r'pokes/add$',views.poke),
    url(r'users/login$',views.login),
    url(r'users/create$',views.create),
    url(r'users/success$',views.success),
    url(r'users/logout$',views.logout),
    url(r'users/(?P<id>\d+)$', views.show),
]
