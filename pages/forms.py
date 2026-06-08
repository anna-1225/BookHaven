from django import forms
from django.core.exceptions import ValidationError
from django.utils.text import slugify
from .models import Book, Category, TagPost


def validate_russian(value):
    allowed_chars = "АБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЬЫЪЭЮЯабвгдеёжзийклмнопрстуфхцчшщбыъэюя0123456789- "
    for char in value:
        if char not in allowed_chars:
            raise ValidationError('Название должно содержать только русские буквы, цифры, дефис и пробел.')


class AddBookForm(forms.Form):
    title = forms.CharField(
        max_length=255,
        min_length=3,
        label="Название книги",
        widget=forms.TextInput(attrs={'class': 'form-input'}),
        validators=[validate_russian]
    )
    slug = forms.SlugField(max_length=255, label="URL (слаг)", required=False)
    author = forms.CharField(max_length=255, label="Автор")
    content = forms.CharField(label="Описание", required=False, widget=forms.Textarea())
    year = forms.IntegerField(label="Год издания", min_value=0, max_value=2026)
    rating = forms.FloatField(label="Рейтинг", min_value=0, max_value=5, required=False)
    is_published = forms.BooleanField(label="Опубликовать", required=False, initial=True)
    cat = forms.ModelChoiceField(queryset=Category.objects.all(), label="Категория", empty_label="Выберите категорию")
    tags = forms.ModelMultipleChoiceField(queryset=TagPost.objects.all(), label="Теги", required=False)


class BookModelForm(forms.ModelForm):
    class Meta:
        model = Book
        fields = ['title', 'slug', 'author', 'content', 'year', 'rating', 'is_published', 'cat', 'tags', 'photo']
        labels = {
            'title': 'Название книги',
            'slug': 'URL (слаг)',
            'author': 'Автор',
            'content': 'Описание',
            'year': 'Год издания',
            'rating': 'Рейтинг',
            'is_published': 'Опубликовать',
            'cat': 'Категория',
            'tags': 'Теги',
            'photo': 'Изображение книги',
        }
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'Введите название',
                'id': 'id_title'
            }),
            'slug': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'vlastelin-kolets',
                'id': 'id_slug'
            }),
            'author': forms.TextInput(attrs={'class': 'form-input', 'placeholder': 'Введите автора'}),
            'content': forms.Textarea(attrs={'class': 'form-textarea', 'rows': 5, 'placeholder': 'Введите описание'}),
            'year': forms.NumberInput(attrs={'class': 'form-input', 'placeholder': '1954'}),
            'rating': forms.NumberInput(attrs={'class': 'form-input', 'step': 0.1}),
            'cat': forms.Select(attrs={'class': 'form-select'}),
            'tags': forms.CheckboxSelectMultiple(),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-file'}),
        }
        help_texts = {
            'slug': 'Только латинские буквы, цифры, дефис и подчеркивание.',
        }

    def clean_title(self):
        title = self.cleaned_data.get('title')
        if len(title) < 3:
            raise ValidationError('Название книги должно содержать минимум 3 символа.')
        return title

    def clean_year(self):
        year = self.cleaned_data.get('year')
        if year and year > 2026:
            raise ValidationError('Год издания не может быть больше текущего.')
        return year


class UploadFileForm(forms.Form):
    file = forms.FileField(
        label="Выберите файл",
        widget=forms.ClearableFileInput(attrs={'class': 'form-file'})
    )