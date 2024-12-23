from django.db import models
from blogs.models import BlogPost
from django.contrib.auth.models import User

# Create your models here.


class Like(models.Model):
    """This model is joined with BlogPost and User model, showing count of the blog"""

    post = models.ForeignKey(BlogPost, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("post", "user")

    def __str__(self):
        return f"{self.user.username} liked {self.post.title}"
