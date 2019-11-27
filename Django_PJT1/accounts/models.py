from django.db import models
from django.urls import reverse

# User < AbstractUser < AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.conf import settings


from django_extensions.db.models import TimeStampedModel
from movies.models import Genre

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit

class User(AbstractUser):
    nickname = models.CharField(max_length=30)
    like_genres = models.ManyToManyField(Genre, related_name='like_users')
    introduction = models.TextField()

class Image(models.Model):
    # Image.objects.get(id=1).user
    # User.objects.get(id=1).image_set.file.
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    file = ProcessedImageField(
        processors=[ResizeToFit(600, 600, mat_color=(256, 256, 256))],
        upload_to = 'users/images/',
        format='JPEG',
        options={'quality': 90},
    )

class Damgle(models.Model):
    page_master = models.ForeignKey(User, on_delete=models.CASCADE, related_name='page_master')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=200)