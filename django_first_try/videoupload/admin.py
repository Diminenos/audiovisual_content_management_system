from django.contrib import admin
from .models import  VideoCategoryModel, VideoDetailModel
# Register your models here.


admin.site.register(VideoCategoryModel)
admin.site.register(VideoDetailModel)