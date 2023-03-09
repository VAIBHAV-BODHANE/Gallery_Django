from django.db import models
from django.contrib.auth.models import AbstractUser


class UserProfile(AbstractUser):
    """User Profile Table"""

    name = models.CharField(max_length=255)
    email = models.CharField(max_length=255, unique=True)
    password = models.CharField(max_length=255)
    username = None

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
    

class UserGallery(models.Model):
    """Master table of the user gallery"""

    user = models.ForeignKey('gallery_app.UserProfile', on_delete=models.CASCADE)
    image_post = models.ImageField(upload_to='userprofile/images/', null=True, blank=True)
    video_post = models.FileField(upload_to='userprofile/videos/', null=True, blank=True)
    post_caption = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.user.email
