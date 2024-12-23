from django.contrib import admin
from .models import BlogPost

# Register your models here.
class BlogAdmin(admin.ModelAdmin):
    list_display = ['title','content','author', 'date_published']
    list_filter = ['title','content','author', 'date_published']
    search_fields = ['title','content','author', 'date_published']

admin.site.register(BlogPost,BlogAdmin)
