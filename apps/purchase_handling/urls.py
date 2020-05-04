from django.urls import path
from apps.purchase_handling.views import *

urlpatterns = [
    path('', PurchaseListView.as_view(), name='purchase_list'),
    path('buy/<int:pk>/', PurchaseCreateView.as_view(), name='purchase_create'),
]
