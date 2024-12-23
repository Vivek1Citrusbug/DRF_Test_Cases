from django import forms
from .models import BlogPost
from django.core.exceptions import ValidationError


class BlogPostForm(forms.ModelForm):
    """This form is used to make a blog for particular user"""

    class Meta:
        model = BlogPost
        fields = ["title", "content"]

    title = forms.CharField(
        max_length=200,
        required=True,
        widget=forms.TextInput(attrs={"class": "form-control"}),
        error_messages={
            "required": "Title is required",
            "max_length": "Title is too long",
        },
    )

    content = forms.CharField(
        widget=forms.Textarea(attrs={"class": "form-control"}),
        required=True,
        error_messages={"required": "Content is required"},
    )

    def clean_content(self):
        content = self.cleaned_data.get("content")
        if len(content) < 20:
            raise ValidationError("Content should be at least 20 characters long.")
        return content
