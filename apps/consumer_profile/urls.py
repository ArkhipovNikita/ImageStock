from django.urls import path, re_path

from .views import *

urlpatterns = [
    re_path('(?P<pk>\d+)/$', ConsumerNewsView.as_view(), name='consumer_news'),
    path('<int:pk>/update/', ConsumerUpdateView.as_view(), name='consumer_update'),
]
