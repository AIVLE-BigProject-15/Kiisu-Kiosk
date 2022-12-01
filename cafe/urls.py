
from django.urls import path, include
from . import views

app_name = 'order'
urlpatterns = [
    path('', views.home, name='home'),
    path('order', views.order, name='order'),
]
