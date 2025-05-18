"""
from django.db import models

# Create your models here.

class Video(models.Model):
    name= models.CharField(max_length=500)
    videofile= models.FileField(upload_to='videos/', null=True, verbose_name="")

    def __str__(self):
        return self.name + ": " + str(self.videofile)
"""

from django.db import models
from django.utils import timezone

from users.models import Profile


class VideoCategoryModel(models.Model):
    category_id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=20)

    def __str__(self):
        return self.category

    class Meta:
        ordering = ('category',)


class VideoDetailModel(models.Model):
    video_id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=1000)
    tags = models.CharField(max_length=1000)
    categories = models.ForeignKey(VideoCategoryModel, on_delete=models.CASCADE,default='1')
    video = models.FileField(upload_to='video/')
    user_id = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='u')
    date_uploaded = models.DateTimeField(default=timezone.now)
    last_modified = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    def __int__(self):
       return self.categories
