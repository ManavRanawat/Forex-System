from django.contrib import admin
from .models import Broker, Order

admin.site.register(Broker)
admin.site.register(Order)