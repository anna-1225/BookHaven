from django import template
from django.utils import timezone
from django.utils.safestring import mark_safe
import random

register = template.Library()

# Данные для тегов
POPULAR_BOOKS = [
    {'id': 1, 'title': 'Властелин колец', 'author': 'Толкин',
     'genre': 'fantasy', 'rating': 4.9},
    {'id': 2, 'title': 'Убийство в экспрессе', 'author': 'Кристи',
     'genre': 'detective', 'rating': 4.8},
    {'id': 3, 'title': 'Преступление и наказание', 'author': 'Достоевский',
     'genre': 'classic', 'rating': 4.7},
    {'id': 4, 'title': 'Гордость и предубеждение', 'author': 'Остин',
     'genre': 'romance', 'rating': 4.6},
]

@register.simple_tag
def current_time(format_string='%H:%M'):
    return timezone.now().strftime(format_string)

@register.simple_tag
def book_rating_stars(rating):
    full = int(rating)
    half = 1 if rating - full >= 0.5 else 0
    empty = 5 - full - half
    stars = '★' * full + '½' * half + '☆' * empty
    return mark_safe(f'<span class="rating-stars">{stars}</span>')

@register.simple_tag
def get_random_books(count=3):
    if count > len(POPULAR_BOOKS):
        count = len(POPULAR_BOOKS)
    return random.sample(POPULAR_BOOKS, count)