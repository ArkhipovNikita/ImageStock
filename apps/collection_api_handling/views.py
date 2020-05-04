from rest_framework import viewsets, permissions

from apps.collection_api_handling.permissions import IsOwnerOrReadOnly
from apps.collection_api_handling.serializers import CollectionSerializer
from apps.collection_handling.models import Collection


class CollectionAPIViewSet(viewsets.ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author_id=self.request.user.id)
