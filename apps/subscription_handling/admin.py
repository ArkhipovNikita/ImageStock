from django.contrib import admin

from apps.subscription_handling.models import Subscription


class SubscriptionInline(admin.StackedInline):
    model = Subscription


@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('who',)
