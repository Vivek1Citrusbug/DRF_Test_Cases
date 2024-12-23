from django import forms
from .models import UserComments


class CommentForm(forms.ModelForm):
    """This form is used to take user comments"""

    class Meta:
        model = UserComments
        fields = ["content"]
        widgets = {
            "content": forms.Textarea(attrs={"rows": 4}),
        }
