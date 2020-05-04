from django.urls import path

from apps.board_handling.views import *

urlpatterns = [
    path('', BoardListView.as_view(), name='board_list'),
    path('create/', BoardCreateView.as_view(), name='board_create'),
    path('<int:pk>/', BoardDetailView.as_view(), name='board_detail'),
    path('<int:pk>/delete', BoardDeleteView.as_view(), name='board_delete'),
    path('<int:pk>/update/', BoardUpdateView.as_view(), name='board_update'),
]
