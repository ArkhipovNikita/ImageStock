from django.contrib import admin

from apps.image_handling.models import Image, Category, Tag


class ImageInline(admin.StackedInline):
    model = Image


class CategoryInline(admin.StackedInline):
    model = Category


class TagInline(admin.StackedInline):
    model = Tag


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):
    list_display = ('author', 'name', 'price', 'created_at', 'purchase_count')
    list_filter = ('price', 'created_at', 'purchase_count')


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = [ImageInline]
