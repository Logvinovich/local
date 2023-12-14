from django import forms
from .models import Post, Comment
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.models import Group


class PostForm(forms.ModelForm):
    text = forms.CharField(min_length=10, widget=CKEditorUploadingWidget())
    class Meta:
        model = Post
        fields = ['title', 'text', 'category']



class MyUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'username']

    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            basic_group = Group.objects.get(name='basic')
            basic_group.user_set.add(user)
        return user


class CommentForm(forms.ModelForm):
    text = forms.CharField(min_length=10)
    class Meta:
        model = Comment
        fields = [ 'post', 'text']


