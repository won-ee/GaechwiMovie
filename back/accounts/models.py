from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill

# Create your models here.
class User(AbstractUser):
    username = models.EmailField(unique=True)
    nickname = models.CharField(max_length=100, unique=True)
    profile_pic = ProcessedImageField(
        blank=True,
        upload_to='profile/images',
        processors=[ResizeToFill(300, 300)],
        format='JPEG',
        options={'quality': 90},
    )