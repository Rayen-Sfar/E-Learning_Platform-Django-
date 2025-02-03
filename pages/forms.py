from django import forms
from .models import Comment, Course, Video1

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={
                'placeholder': 'Enter your comment',
                'required': True,
                'maxlength': 1000,
                'cols': 30,
                'rows': 10,
            })
        }



class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['title', 'description', 'thumbnail']

class Video1Form(forms.ModelForm):
    class Meta:
        model = Video1
        fields = ['title', 'video_file', 'poster_image']