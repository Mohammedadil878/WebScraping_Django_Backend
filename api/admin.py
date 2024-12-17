from django.contrib import admin

from .models import ScrapedData

# Register your models here.
admin.site.register(ScrapedData)

# @admin.register(ScrapedData)
# class ScrapedDataAdmin(admin.ModelAdmin):
#     list_display = ['id', 'url', 'title', 'content', 'ScrapedAt']