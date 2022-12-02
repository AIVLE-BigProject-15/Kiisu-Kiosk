
from django.urls import path, include
from . import views

app_name = 'cafe'
urlpatterns = [
    path('', views.home, name='home'),
    path('order', views.order, name='order'),
    path('temp', views.temp, name='temp'),
]


