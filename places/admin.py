from django.contrib import admin

from places.models import Company, Image


class ImageInline(admin.TabularInline):
    model = Image


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    inlines = [
        ImageInline,
    ]


admin.site.register(Image)
