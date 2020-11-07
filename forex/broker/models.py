from django.db import models
from django.urls import reverse

class Broker(models.Model):
    title  = models.CharField(max_length = 200)
    country = models.CharField(max_length = 200)
    description = models.CharField(max_length = 500, default=None)
    rate = models.FloatField(null=True, blank=True)
    phone_number = models.CharField(max_length=12)
    image_url = models.CharField(max_length = 2083, default=False)
    broker_available = models.BooleanField(default=False)

    def __str__(self):
        return self.title


class Order(models.Model):
	product = models.ForeignKey(Broker, max_length=200, null=True, blank=True, on_delete = models.SET_NULL)
	created =  models.DateTimeField(auto_now_add=True) 

	def __str__(self):
		return self.product.title