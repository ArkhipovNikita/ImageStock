from django.urls import path
from apps.subscription_handling.views import *

urlpatterns = [
    path('<int:pk>/subscribe/', SubscriptionView.as_view(), name='subscribe'),
    path('<int:pk>/unsubscribe/', UnsubscriptionView.as_view(), name='unsubscribe'),
]
