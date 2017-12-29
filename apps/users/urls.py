from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'main$', views.index),
    url(r'dashboard$',views.dashboard),
    url(r'wish_items/add$',views.add_item),
    url(r'wish_items/create$',views.insert),
    url(r'users/login$',views.login),
    url(r'users/create$',views.create),
    url(r'users/success$',views.success),
    url(r'users/logout$',views.logout),
    url(r'wish_items/(?P<id>\d+)$', views.show),
    url(r'wish_items/add_wish$',views.add_wish),
    url(r'wish_items/del_wish$',views.del_wish),
]
