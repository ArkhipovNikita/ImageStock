from django.urls import path
from apps.collection_handling.views import *

urlpatterns = [
    path('create/', CollectionCreateView.as_view(), name='collection_create'),
    path('<int:pk>/', CollectionDetailView.as_view(), name='collection_detail'),
    path('collection/<int:pk>/delete', CollectionDeleteView.as_view(), name='collection_delete'),
    path('collection/<int:pk>/update/', CollectionUpdateView.as_view(), name='collection_update'),
]
