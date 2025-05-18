"""
from django import forms
from .models import Video

class VideoForm(forms.ModelForm):
    class Meta:
        model= Video
        fields= ["name", "videofile"]

"""
from django import forms
from .models import VideoDetailModel


class VideoDetailForm(forms.ModelForm):
    class Meta:
        model = VideoDetailModel
        fields = ("video", "title", "description", "categories", "tags")
        widgets = {
            'video': forms.FileInput(attrs={'accept': 'video/*', 'class': 'form-control'}),
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description'}),
            'categories': forms.Select(attrs={'class': 'form-control'}),
            'tags': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Tags'}),
        }
