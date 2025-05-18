"""
from django.shortcuts import render
from .models import Video
from .forms import VideoForm
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def showvideo(request):

    lastvideo= Video.objects.last()

    if lastvideo:
        videofile=lastvideo.videofile
    
    else:
        videofile= None


    form= VideoForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()

    
    context= {'videofile': videofile,
              'form': form
              }
    
      
    return render(request, 'videoupload/videos.html', context)
"""
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.views.generic import (CreateView, DetailView, UpdateView, DeleteView)
from django_filters.views import FilterView

from videoupload.filters import CategoryFilter
from videoupload.forms import VideoDetailForm
from videoupload.models import VideoDetailModel

class UploadVideo(LoginRequiredMixin, CreateView):
    login_url = '/login/'
    form_class = VideoDetailForm
    template_name = "videos.html"
    success_url = '/home/'

    def form_valid(self, form):
        form.instance.user_id = self.request.user
        return super(UploadVideo, self).form_valid(form)


class MyVideos(LoginRequiredMixin, FilterView, Paginator):
    filterset_class = CategoryFilter
    login_url = '/login/'
    template_name = 'my_videos.html'
    model = VideoDetailModel
    paginate_by = 25

    def get_context_data(self, **kwargs):
        context = super(MyVideos, self).get_context_data(**kwargs)
        context['user_full_name'] = self.request.user.full_name
        context['user_email'] = self.request.user.email
        return context

    def get_queryset(self):
        queryset = super(MyVideos, self).get_queryset()
        queryset = queryset.filter(user_id_id=self.request.user.user_id).order_by('date_uploaded')
        return queryset




class DeleteVideo(LoginRequiredMixin, DeleteView):
    template_name = 'delete_video.html'
    form_class = VideoDetailForm
    success_url = '/my_videos/'

    def get_object(self, **kwargs):
        return VideoDetailModel.objects.get(pk=self.request.GET.get('video_id'))


class EditVideoDetails(LoginRequiredMixin, UpdateView):
    template_name = 'edit_video_details.html'
    form_class = VideoDetailForm

    def get_success_url(self):
        success_url = '/edit_video_details/?video_id=' + self.request.GET.get('video_id')
        return success_url

    def get_object(self, **kwargs):
        return VideoDetailModel.objects.get(pk=self.request.GET.get('video_id'))
