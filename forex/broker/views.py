from django.shortcuts import render 
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView
from django.contrib.auth.mixins import LoginRequiredMixin 
from .models import Broker, Order
from django.urls import reverse_lazy
from django.db.models import Q # for search method
from django.http import JsonResponse
import json



class BrokersListView(ListView):
    model = Broker
    template_name = 'list.html'


class BrokersDetailView(DetailView):
    model = Broker
    template_name = 'detail.html'


class SearchResultsListView(ListView):
	model = Broker
	template_name = 'search_results.html'

	def get_queryset(self): # new
		query = self.request.GET.get('q')
		return sorted(Broker.objects.filter(
		Q(title__icontains=query) | Q(country__icontains=query)
		) , key = lambda x : x.rate)

class BrokerCheckoutView(LoginRequiredMixin, DetailView):
    model = Broker
    template_name = 'checkout.html'
    login_url     = 'login'


def paymentComplete(request):
	body = json.loads(request.body)
	print('BODY:', body)
	product = Broker.objects.get(id=body['productId'])
	Order.objects.create(
		product=product
	)
	return JsonResponse('Payment completed!', safe=False)