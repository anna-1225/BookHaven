from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from pages.models import Book

GENRES = [
    {'id': 1, 'name': 'Фэнтези', 'slug': 'fantasy', 'book_count': 45},
    {'id': 2, 'name': 'Детектив', 'slug': 'detective', 'book_count': 32},
    {'id': 3, 'name': 'Классика', 'slug': 'classic', 'book_count': 28},
    {'id': 4, 'name': 'Роман', 'slug': 'romance', 'book_count': 37},
]


def index(request):
    books = Book.published.all()[:3]
    total_books = Book.published.count()

    context = {
        'title': 'Главная страница книжного форума BookHaven',
        'posts': books,
        'genres': GENRES,
        'online_users': 42,
        'selected_genre': 0,
        'total_books': total_books,
        'total_users': 1234,
    }
    return render(request, 'pages/index.html', context)


def genres_list(request):
    total_books = Book.published.count()

    context = {
        'title': 'Литературные жанры',
        'genres': GENRES,
        'online_users': 42,
        'selected_genre': 0,
        'total_books': total_books,
        'total_users': 1234,
    }
    return render(request, 'pages/genres.html', context)


def genre_detail(request, genre_slug):
    valid_genres = ['fantasy', 'detective', 'classic', 'romance']
    if genre_slug not in valid_genres:
        raise Http404("Жанр не найден")

    genre = next((g for g in GENRES if g['slug'] == genre_slug), None)
    books = Book.published.filter(genre=genre_slug)
    total_books = Book.published.count()

    context = {
        'title': f'Книги жанра {genre["name"]}',
        'genre_name': genre['name'],
        'genre_slug': genre_slug,
        'books': books,
        'genres': GENRES,
        'online_users': 42,
        'selected_genre': genre['id'],
        'total_books': total_books,
        'total_users': 1234,
    }
    return render(request, 'pages/genre_detail.html', context)


def book_detail(request, book_slug):
    book = get_object_or_404(Book, slug=book_slug, is_published=Book.Status.PUBLISHED)

    comment_id = request.GET.get('comment_id', '')

    COMMENTS = [
        {'id': 1, 'author': 'BookLover', 'date': '2026-01-15 14:30',
         'text': 'Отличная книга! Очень понравилось обсуждение на форуме.', 'likes': 5},
        {'id': 2, 'author': 'Reader123', 'date': '2026-01-16 09:45',
         'text': 'Очень понравилось обсуждение.', 'likes': 3},
        {'id': 3, 'author': 'BookWorm', 'date': '2026-01-16 18:20',
         'text': 'Жду продолжения!', 'likes': 2},
    ]

    filtered_comments = COMMENTS
    if comment_id:
        filtered_comments = [c for c in COMMENTS if c['id'] == int(comment_id)]

    genre = next((g for g in GENRES if g['slug'] == book.genre), None)
    total_books = Book.published.count()

    context = {
        'title': f'{book.title}',
        'genre_name': genre['name'] if genre else book.genre,
        'book': book,
        'comments': filtered_comments,
        'genres': GENRES,
        'online_users': 42,
        'selected_genre': genre['id'] if genre else 0,
        'total_books': total_books,
        'total_users': 1234,
    }
    return render(request, 'pages/book_detail.html', context)


def old_catalog_redirect(request):
    return redirect('genres')


def books_by_year(request, pub_year):
    if pub_year <= 0:
        return redirect('home')

    books_in_year = Book.published.filter(year=pub_year)
    total_books = Book.published.count()

    context = {
        'title': f'Книги {pub_year} года',
        'pub_year': pub_year,
        'books': books_in_year,
        'genres': GENRES,
        'online_users': 42,
        'selected_genre': 0,
        'total_books': total_books,
        'total_users': 1234,
    }
    return render(request, 'pages/books_by_year.html', context)