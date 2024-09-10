from django.contrib import admin
from django.utils.safestring import mark_safe

from django.db import models
from .models import Women, Category, TagPost

from tinymce.widgets import TinyMCE

# Register your models here.
#admin.site.register(Women)

@admin.register(Women)
class WomenAdmin(admin.ModelAdmin):
    save_on_top = True
    ordering = ['time_create', 'title']
    readonly_fields = ['post_photo']
    list_display = ('id', 'title', 'post_photo', 'time_create', 'cat', 'is_published')
    list_display_links = ('id', 'title')
    list_editable = ('cat', 'is_published')

    @admin.display(description='Изображение', ordering='content')
    def post_photo(self, women: Women):
        if women.photo:
            return mark_safe(f"<img src='{women.photo.url}' width=50>")
        return 'Без фото'

    formfield_overrides = {
        models.TextField: {'widget': TinyMCE()}
    }

class TagsInline(admin.StackedInline):
    model = Women.tags.through

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    list_display_links = ('id', 'name')

@admin.register(TagPost)
class TagPostAdmin(admin.ModelAdmin):
    list_display = ('tag', 'slug')
    #list_display_links = ('id', 'name')
    inlines = [
        TagsInline,
    ]
    exclude = ["tags"]


