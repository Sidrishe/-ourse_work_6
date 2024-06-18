from django import forms

from blog.models import Blog
from users.forms import StyleFormMixin


class BlogForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = Blog
        fields = ('title', 'content', 'image', 'creation_date', 'publication_feature')