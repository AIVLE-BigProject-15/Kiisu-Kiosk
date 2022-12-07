
from django.urls import path, include
from . import views

app_name = 'cafe'
urlpatterns = [
    path('', views.home, name='home'),
    path('order', views.order, name='order'),
    # path('camera', views.camera, name='camera'),
    path('detect_age_group', views.detect_age_group, name='detect_age_group'),
]


