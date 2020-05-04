from django.urls import path
from apps.author_profile.views import *

urlpatterns = [
    path('<int:pk>/', AuthorDetailImageListView.as_view(), name='author_detail_image'),
    path('<int:pk>/collections/', AuthorDetailCollectionListView.as_view(), name='author_detail_collection'),
    path('<int:pk>/update', AuthorUpdateView.as_view(), name='author_update'),
]
