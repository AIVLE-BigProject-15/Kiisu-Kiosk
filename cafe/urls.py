
from django.urls import path, include

# from . import views
# from .views import fetch_user
# app_name = 'cafe'
# urlpatterns = [
#     path('', views.home, name='home'),
#     path('young_order', views.young_order, name='young_order'),
#     path('old_order', views.old_order, name='old_order'),
#     path('young_confirm', views.young_confirm, name='young_confirm'),
#     path('old_confirm', views.old_confirm, name='old_confirm'),
#     path('young_pay', views.young_pay, name='young_pay'),
#     path('old_pay', views.old_pay, name='old_pay'),
#     path('detect_age_group', views.detect_age_group, name='detect_age_group'),
#     path('fetch_user', fetch_user.as_view(), name='user'),
#     path('camera', views.camera, name='camera'),
# ]

from . import views_jh
from .views_jh import fetch_user
app_name = 'cafe'
urlpatterns = [
    path('', views_jh.home, name='home'),
    path('young_order', views_jh.young_order, name='young_order'),
    path('old_order', views_jh.old_order, name='old_order'),
    path('young_confirm', views_jh.young_confirm, name='young_confirm'),
    path('old_confirm', views_jh.old_confirm, name='old_confirm'),
    path('young_pay', views_jh.young_pay, name='young_pay'),
    path('old_pay', views_jh.old_pay, name='old_pay'),
    path('detect_age_group', views_jh.detect_age_group, name='detect_age_group'),
    path('fetch_user', fetch_user.as_view(), name='user'),
    path('camera', views_jh.camera, name='camera'),
]


