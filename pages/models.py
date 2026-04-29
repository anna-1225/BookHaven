from django.db import models
from django.urls import reverse
from django.utils.text import slugify
from django.contrib.auth.models import User


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(is_published=Book.Status.PUBLISHED)


class Category(models.Model):
    name = models.CharField(max_length=100, db_index=True, verbose_name="Название")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('category', kwargs={'cat_slug': self.slug})

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class TagPost(models.Model):
    tag = models.CharField(max_length=100, db_index=True, verbose_name="Тег")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")

    def __str__(self):
        return self.tag

    def get_absolute_url(self):
        return reverse('tag', kwargs={'tag_slug': self.slug})

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'


class Book(models.Model):
    class Status(models.IntegerChoices):
        DRAFT = 0, 'Черновик'
        PUBLISHED = 1, 'Опубликовано'

    title = models.CharField(max_length=255, verbose_name="Название")
    slug = models.SlugField(max_length=255, unique=True, db_index=True, verbose_name="URL")
    author = models.CharField(max_length=255, verbose_name="Автор")
    content = models.TextField(blank=True, verbose_name="Описание")
    genre = models.CharField(max_length=50, blank=True, default='', verbose_name="Жанр")
    year = models.IntegerField(default=2000, verbose_name="Год издания")
    rating = models.FloatField(default=0.0, verbose_name="Рейтинг")
    time_create = models.DateTimeField(auto_now_add=True, verbose_name="Время создания")
    time_update = models.DateTimeField(auto_now=True, verbose_name="Время обновления")
    is_published = models.IntegerField(choices=Status.choices, default=Status.DRAFT, verbose_name="Статус")

    cat = models.ForeignKey(Category, on_delete=models.PROTECT, null=True, blank=True, related_name='books', verbose_name="Категория")
    tags = models.ManyToManyField(TagPost, blank=True, related_name='books', verbose_name="Теги")

    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book_detail', kwargs={'book_slug': self.slug})

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-time_create']
        verbose_name = 'Книга'
        verbose_name_plural = 'Книги'


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name="Пользователь")
    bio = models.TextField(blank=True, verbose_name="О себе")
    birth_date = models.DateField(blank=True, null=True, verbose_name="Дата рождения")

    def __str__(self):
        return f"Профиль пользователя {self.user.username}"

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'