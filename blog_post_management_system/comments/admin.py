from django.contrib import admin
from .models import UserComments

# Register your models here.
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post_id','user_id','content','date_posted']
    list_filter = ['post_id','user_id','content','date_posted']
    search_fields = ['user_id','content','date_posted']

admin.site.register(UserComments,CommentAdmin)

