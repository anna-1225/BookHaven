from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Book.Status.PUBLISHED)


class Book(models.Model):
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, db_index=True)
    author = models.CharField(max_length=255)
    content = models.TextField(blank=True)
    genre = models.CharField(max_length=50, blank=True, default='')
    year = models.IntegerField(default=2000)
    rating = models.FloatField(default=0.0)
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(choices=Status.choices, default=Status.DRAFT)
    cat = models.ForeignKey('Category', on_delete=models.PROTECT, related_name='books', verbose_name="Категория")
    tags = models.ManyToManyField('TagPost', blank=True, related_name='books', verbose_name="Теги")

    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book_detail', kwargs={'book_slug': self.slug})
    class Meta:
        ordering = ['-time_create']

class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Название")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class TagPost(models.Model):
    tag = models.CharField(max_length=100, db_index=True, verbose_name="Тег")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.tag

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug': self.slug})

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"



class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name="Пользователь")
    bio = models.TextField(blank=True, verbose_name="О себе")
    birth_date = models.DateField(blank=True, null=True, verbose_name="Дата рождения")

    def __str__(self):
        return f"Профиль пользователя {self.user.username}"

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"