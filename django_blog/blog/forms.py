from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Profile, Post, Comment
from taggit.forms import TagWidget

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Required")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ("bio", "profile_photo")

class PostForm(forms.ModelForm):
    tags_input = forms.CharField(required=False, label="Tags (comma seperated)", help_text="Enter tags")

    class Meta:
        model = Post
        fields = ["title", "content"] 
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "content": forms.Textarea(attrs={"class": "form-control", "rows": 8}),
            "tags": TagWidget(),
        }

        def __init__(self, *args, **kwargs):
    
            super().__init__(*args, **kwargs)
            if self.instance and self.instance.pk:
                self.fields["tags_input"].initial = ", ".join(
                    [t.name for t in self.instance.tags.all()]
            )

    def save(self, commit=True):
        
        post = super().save(commit=commit)
        
        return post

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(attrs={"rows": 4, "class": "form-control"}),
        }
