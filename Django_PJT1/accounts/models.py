from django.db import models
from django.urls import reverse
# User < AbstractUser < AbstractBaseUser
from django.contrib.auth.models import AbstractUser
from django.conf import settings
from movies.models import Genre

from django_extensions.db.models import TimeStampedModel

from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFit

class User(AbstractUser):
    nickname = models.Charfield(max_length=30)
    like_genres = models.ManyToManyField(Genre, related_name='like_users')
    introduction = models.TextField()

class Chatroom(models.Model):
    name = models.Charfield(max_length=200)
    chat_users = models.ManyToManyField(User, related_name='use_chatroom')
    styles = models.ManyToManyField(Genre, related_name='chats')

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

class Chatcontents(TimeStampedModel):
    content = models.Charfield(max_length=300)
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    chatroom = models.ForeignKey(Chatroom, on_delete=models.CASCADE)