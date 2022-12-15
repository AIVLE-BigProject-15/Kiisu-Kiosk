
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


