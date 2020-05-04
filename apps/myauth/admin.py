from django.contrib import admin

from apps.board_handling.admin import BoardInline
from apps.collection_handling.admin import CollectionInline
from apps.myauth.models import Author, Consumer


class AuthorInline(admin.StackedInline):
    model = Author


class ConsumerInline(admin.StackedInline):
    model = Consumer


class UserAdmin(admin.ModelAdmin):
    def __init__(self, *args, **kwargs):
        super(UserAdmin, self).__init__(*args, **kwargs)
        self.list_display = ('email', 'username', 'created_at', 'is_active', 'is_staff',)
        self.list_filter = ('created_at', 'is_active', 'is_staff',)


@admin.register(Author)
class AuthorAdmin(UserAdmin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.list_display += ('first_name', 'last_name')
        self.inlines = [CollectionInline]


@admin.register(Consumer)
class ConsumerAdmin(UserAdmin):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.inlines = [BoardInline]
