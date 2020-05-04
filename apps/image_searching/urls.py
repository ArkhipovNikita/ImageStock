from django.urls import path
from apps.image_searching.views import *

urlpatterns = [
    path('', SearchView.as_view(), name='search'),
    path('search/', SearchResultView.as_view(), name='search_result'),
]
