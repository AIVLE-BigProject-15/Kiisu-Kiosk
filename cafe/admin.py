from django.contrib import admin
from django.conf import settings
from .models import *

admin.site.register(Menu)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(Model)
