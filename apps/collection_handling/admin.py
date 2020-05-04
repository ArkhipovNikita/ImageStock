from django.contrib import admin

from apps.collection_handling.models import Collection


class CollectionInline(admin.StackedInline):
    model = Collection


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'created_at', 'changed_at')
    list_filter = ('author', 'created_at', 'changed_at')
