from django.urls import path
from django.contrib import admin
from django.contrib.auth import views as auth_views 
from django.urls import path, include 
from users import views as user_views
from . import views
from django.conf.urls.static import static
from django.conf import settings
from videoupload import views as video_views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.homepage, name='ArUTv-home'),
    path('register/', user_views.register, name='register'),
    path('profile/', user_views.profile, name='profile'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('videoupload/',video_views.UploadVideo.as_view(template_name='videoupload/videos.html'), name='video-upload'),
    path('my_videos/', video_views.MyVideos.as_view(template_name='videoupload/my_videos.html'), name='my_videos'),
    path('edit_video_details/', video_views.EditVideoDetails.as_view(template_name='videoupload/edit_video_details.html'), name='edit_video_details'),
    path('delete_video/', video_views.DeleteVideo.as_view(template_name='videoupload/delete_video.html'), name='delete_video'),
] + static(settings.MEDIA_URL, document_root= settings.MEDIA_ROOT)