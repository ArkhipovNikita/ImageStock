from django.urls import path
from apps.image_handling.views import *

urlpatterns = [
    path('upload/', ImageCreateFormView.as_view(), name='image_upload'),
    path('<int:pk>/', ImageDetailView.as_view(), name='image_detail'),
    path('<int:pk>/delete', ImageDeleteView.as_view(), name='image_delete'),
    path('<int:pk>/update/', ImageUpdateFormView.as_view(), name='image_update'),
]
