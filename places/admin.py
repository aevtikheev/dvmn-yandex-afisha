from django.contrib import admin
from django.utils.html import format_html
from adminsortable2.admin import SortableInlineAdminMixin

from places.models import Company, Image


class ImageInline(SortableInlineAdminMixin, admin.TabularInline):
    model = Image
    readonly_fields = ['preview_image']

    def preview_image(self, obj):
        return format_html('<img src="{}" height=200/>', obj.image.url)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    inlines = [
        ImageInline,
    ]


@admin.register(Image)
class ImageAdmin(admin.ModelAdmin):

    readonly_fields = ['preview_image']

    def preview_image(self, obj):
        return format_html('<img src="{}" />', obj.image.url)
