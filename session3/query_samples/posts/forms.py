from django import forms
from django.core.exceptions import ValidationError
from django.forms import modelformset_factory

from posts.models import Post, Book


def validate_title(value):
    if value == 'post':
        raise ValidationError('title is not valid')
    return value


# class PostForm(forms.Form):
#     title = forms.CharField(max_length=10, initial='write here...', validators=[validate_title])
#     content = forms.CharField(widget=forms.Textarea(), label='post text')
#     templates = forms.ModelChoiceField(queryset=PostTemplate.objects.all())
#
#     def clean_title(self):
#         title = self.cleaned_data['title']
#         if title == 'POST':
#             raise ValidationError('title should not be POST')
#         return title
#
#     def clean(self):
#         try:
#             if self.cleaned_data['title'] == self.cleaned_data['content']:
#                 raise ValidationError('title must be different from content')
#         except:
#             raise ValidationError('keys do not exist')

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'templates', 'author']


# post_formset = formset_factory(PostForm, extra=3)
post_formset = modelformset_factory(Post, PostForm, extra=2, can_delete=True, can_delete_extra=True)


class BookForm(forms.ModelForm):
    published_date = forms.DateTimeField()

    class Meta:
        model = Book
        fields = ['title', 'published_date', 'author']


book_formset = modelformset_factory(Book, BookForm, can_delete=True, extra=1)
