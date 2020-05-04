from django.contrib import admin

from apps.board_handling.models import Board


class BoardInline(admin.StackedInline):
    model = Board


@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'created_at', 'changed_at')
    list_filter = ('owner', 'created_at', 'changed_at')
