
from django.urls import path, include

from . import views
from .views import fetch_user
app_name = 'cafe'
urlpatterns = [
    path('', views.home, name='home'),
    path('order', views.order, name='order'),
    path('confirm', views.confirm, name='confirm'),
    path('pay', views.pay, name='pay'),
    path('detect_age_group', views.detect_age_group, name='detect_age_group'),
    path('fetch_user', fetch_user.as_view(), name='user'),
    path('camera', views.camera, name='camera'),
]

# from . import views_jh
# from .views_jh import fetch_user
# app_name = 'cafe'
# urlpatterns = [
#     path('', views_jh.home, name='home'),
#     path('order', views_jh.order, name='order'),
#     path('confirm', views_jh.confirm, name='confirm'),
#     path('pay', views_jh.pay, name='pay'),
#     path('detect_age_group', views_jh.detect_age_group, name='detect_age_group'),
#     path('fetch_user', fetch_user.as_view(), name='user'),
#     path('camera', views_jh.camera, name='camera'),

# ]


