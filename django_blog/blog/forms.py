from django import forms
from django.contrib.auth.models import User
from .models import Profile
from models import Post, Comment, Tag  

class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['image']

class PostForm(forms.ModelForm):
    # allow user to add tags as comma-separated names
    tags_field = forms.CharField(
        required=False,
        label='Tags',
        help_text='Comma-separated tags (e.g. django,python,web).'
    )

    class Meta:
        model = Post
        fields = ['title', 'content', 'published']

    def __init__(self, *args, **kwargs):
        # if editing an existing post, populate tags_field with existing tags
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.pk:
            self.fields['tags_field'].initial = ', '.join(t.name for t in self.instance.tags.all())

    def save(self, commit=True, user=None):
        # save Post first, then handle tags
        post = super().save(commit=False)
        if user and not post.pk:
            post.author = user
        if commit:
            post.save()
        # handle tags string
        tag_names = [t.strip() for t in (self.cleaned_data.get('tags_field') or '').split(',') if t.strip()]
        tags = []
        for name in tag_names:
            tag_obj, created = Tag.objects.get_or_create(name__iexact=name, defaults={'name': name})
            # get_or_create with case-insensitive: fallback since get_or_create doesn't support case-insensitive directly
            if created is False and tag_obj.name.lower() != name.lower():
                # ensure canonical capitalization if needed
                pass
            tags.append(tag_obj)
        # assign tags
        if commit:
            post.tags.set(tags)
        else:
            # if not committing, attach tags later
            self._pending_tags = tags
        return post 


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }