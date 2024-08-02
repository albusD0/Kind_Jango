from django.contrib import admin

from .models import Women, Category


# Register your models here.
#admin.site.register(Women)

@admin.register(Women)
class WomenAdmin(admin.ModelAdmin):
    ordering = ['time_create', 'title']
    list_display = ('id', 'title', 'time_create', 'is_published')
    list_display_links = ('id', 'title')

    list_editable = ('is_published',)

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')



