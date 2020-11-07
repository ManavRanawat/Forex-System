from django.urls import path
from .views import BrokersListView, BrokersDetailView, BrokerCheckoutView, paymentComplete, SearchResultsListView


urlpatterns = [
    path('', BrokersListView.as_view(), name = 'list'),
    path('<int:pk>/', BrokersDetailView.as_view(), name = 'detail'),
    path('<int:pk>/checkout/', BrokerCheckoutView.as_view(), name = 'checkout'),
    path('complete/', paymentComplete, name = 'complete'),
    path('search/', SearchResultsListView.as_view(), name = 'search_results'),
]