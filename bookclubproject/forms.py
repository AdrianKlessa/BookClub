from django import forms

from .models import BookComment


class BookCommentForm(forms.ModelForm):

    class Meta:

        model = BookComment

        exclude = ("user_profile", "book", "published_datetime", "hidden")

        labels = {
            "comment": "Add a comment",
        }