from django.contrib import admin

from apps.purchase_handling.models import Purchase


class PurchaseInline(admin.StackedInline):
    model = Purchase


@admin.register(Purchase)
class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('buyer', 'seller', 'total', 'created_at',)
    list_filter = ('created_at', )
