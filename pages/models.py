from django.db import models
from django.urls import reverse


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

    objects = models.Manager()
    published = PublishedManager()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book_detail', kwargs={'book_slug': self.slug})
    class Meta:
        ordering = ['-time_create']