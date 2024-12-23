from django.db import models
from blogs.models import BlogPost
from django.contrib.auth.models import User
from django.utils import timezone

# Create your models here.


class UserComments(models.Model):
    """This model is joined with User and BlogPost model, describing user comments on particular post"""

    post_id = models.ForeignKey(BlogPost, on_delete=models.CASCADE,related_name='comments')
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=257)
    date_posted = models.DateField(default=timezone.now)

    def __str__(self):
        return f"""{self.user_id.username} : {self.content}         Date Published : {self.date_posted.strftime('%Y-%m-%d')}"""
