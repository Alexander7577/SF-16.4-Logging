from django import forms
from django.core.exceptions import ValidationError
from .models import Post, Category


class NewsForm(forms.ModelForm):
    post_category = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label='Категории:'
    )

    class Meta:
        model = Post
        fields = [
            'author',
            'post_type',
            'post_category',
            'title',
            'content',
        ]

    def clean(self):
        cleaned_data = super().clean()
        content = cleaned_data.get('content')
        if len(content) < 50:
            raise ValidationError('Контент не может содержать меньше 50 символов!')
        return cleaned_data
