from django.db import models
from django.contrib.auth.models import User  


class UserProfile(models.Model):
    """This model is joined with built in User model"""

    user = models.OneToOneField(User, on_delete=models.CASCADE)  
    bio = models.TextField(blank=True)  
    profile_picture = models.ImageField(upload_to='profiles/profile_pictures/', blank=True, null=True)  

    def __str__(self):
        return f"{self.user.username}'s Profile"
