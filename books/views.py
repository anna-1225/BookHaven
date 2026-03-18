from django.http import HttpResponse, Http404
from django.shortcuts import render, redirect

# Данные для демонстрации
GENRES = [
    {'id': 1, 'name': 'Фэнтези', 'slug': 'fantasy', 'book_count': 45},
    {'id': 2, 'name': 'Детектив', 'slug': 'detective', 'book_count': 32},
    {'id': 3, 'name': 'Классика', 'slug': 'classic', 'book_count': 28},
    {'id': 4, 'name': 'Роман', 'slug': 'romance', 'book_count': 37},
]

BOOKS = {
    'fantasy': [
        {'id': 1, 'title': 'Властелин колец', 'author': 'Дж.Р.Р. Толкин',
         'year': 1954, 'rating': 4.9, 'genre_slug': 'fantasy',
         'description': 'Эпическая сага о борьбе добра со злом в Средиземье.'},
        {'id': 2, 'title': 'Игра престолов', 'author': 'Джордж Мартин',
         'year': 1996, 'rating': 4.8, 'genre_slug': 'fantasy',
         'description': 'Политические интриги и войны за власть в Вестеросе.'},
    ],
    'detective': [
        {'id': 3, 'title': 'Убийство в Восточном экспрессе', 'author': 'Агата Кристи',
         'year': 1934, 'rating': 4.8, 'genre_slug': 'detective',
         'description': 'Знаменитый детектив Эркюль Пуаро расследует убийство в поезде.'},
    ],
    'classic': [
        {'id': 4, 'title': 'Преступление и наказание', 'author': 'Ф.М. Достоевский',
         'year': 1866, 'rating': 4.7, 'genre_slug': 'classic',
         'description': 'Философский роман о преступлении и моральном возрождении.'},
    ],
    'romance': [
        {'id': 5, 'title': 'Гордость и предубеждение', 'author': 'Джейн Остин',
         'year': 1813, 'rating': 4.6, 'genre_slug': 'romance',
         'description': 'История любви и преодоления предрассудков.'},
    ],
}


def index(request):
    """Главная страница"""
    # Собираем все книги для отображения на главной
    all_posts = []
    for genre_slug, books_list in BOOKS.items():
        for book in books_list:
            all_posts.append(book)

    context = {
        'title': 'Главная страница книжного форума BookHaven',
        'posts': all_posts[:3],  # первые 3 книги
        'genres': GENRES,
        'online_users': 42,
        'selected_genre': 0,
        'total_books': sum(genre['book_count'] for genre in GENRES),
        'total_users': 1234,
    }
    return render(request, 'pages/index.html', context)


def genres_list(request):
    """Страница со списком литературных жанров"""
    context = {
        'title': 'Литературные жанры',
        'genres': GENRES,
        'online_users': 42,
        'selected_genre': 0,
        'total_books': sum(genre['book_count'] for genre in GENRES),
        'total_users': 1234,
    }
    return render(request, 'pages/genres.html', context)


def genre_detail(request, genre_slug):
    """Страница книг определенного жанра"""
    valid_genres = ['fantasy', 'detective', 'classic', 'romance']
    if genre_slug not in valid_genres:
        raise Http404("Жанр не найден")

    # Находим жанр по slug
    genre = next((g for g in GENRES if g['slug'] == genre_slug), None)
    books = BOOKS.get(genre_slug, [])

    context = {
        'title': f'Книги жанра {genre["name"]}',
        'genre_name': genre['name'],
        'genre_slug': genre_slug,
        'books': books,
        'genres': GENRES,
        'online_users': 42,
        'selected_genre': genre['id'],
        'total_books': sum(genre['book_count'] for genre in GENRES),
        'total_users': 1234,
    }
    return render(request, 'pages/genre_detail.html', context)


def book_detail(request, genre_slug, book_id):
    """Страница конкретной книги"""
    if int(book_id) > 10:
        raise Http404("Книга не найдена")

    comment_id = request.GET.get('comment_id', '')

    print(f"[DEBUG] GET-параметр comment_id = {comment_id}")
    print(f"[DEBUG] Все GET-параметры: {request.GET}")

    # Получаем информацию о книге
    books = BOOKS.get(genre_slug, [])
    book = next((b for b in books if b['id'] == int(book_id)), None)

    if not book:
        raise Http404("Книга не найдена")

    # Находим жанр
    genre = next((g for g in GENRES if g['slug'] == genre_slug), None)

    # Комментарии
    COMMENTS = [
        {'id': 1, 'author': 'BookLover', 'date': '2024-01-15 14:30',
         'text': 'Отличная книга! Очень понравилось обсуждение на форуме.', 'likes': 5},
        {'id': 2, 'author': 'Reader123', 'date': '2024-01-16 09:45',
         'text': 'Очень понравилось обсуждение. Много интересных мыслей.', 'likes': 3},
        {'id': 3, 'author': 'BookWorm', 'date': '2024-01-16 18:20',
         'text': 'Жду продолжения! Когда будет следующая встреча клуба?', 'likes': 2},
    ]

    # Фильтруем комментарии если указан comment_id
    filtered_comments = COMMENTS
    if comment_id:
        filtered_comments = [c for c in COMMENTS if c['id'] == int(comment_id)]

    context = {
        'title': f'{book["title"]} - обсуждение книги',
        'genre_name': genre['name'],
        'genre_slug': genre_slug,
        'book': book,
        'comments': filtered_comments,
        'genres': GENRES,
        'online_users': 42,
        'selected_genre': genre['id'],
        'total_books': sum(genre['book_count'] for genre in GENRES),
        'total_users': 1234,
    }
    return render(request, 'pages/book_detail.html', context)


def old_catalog_redirect(request):
    """Редирект со старого каталога"""
    return redirect('genres')


def books_by_year(request, pub_year):
    """Книги, изданные в определенном году"""
    if pub_year <= 0:
        return redirect('home')

    # Собираем все книги, изданные в указанном году
    books_in_year = []
    for genre_slug, books_list in BOOKS.items():
        for book in books_list:
            if book['year'] == pub_year:
                books_in_year.append(book)

    context = {
        'title': f'Книги {pub_year} года',
        'pub_year': pub_year,
        'books': books_in_year,
        'genres': GENRES,
        'online_users': 42,
        'selected_genre': 0,
        'total_books': sum(genre['book_count'] for genre in GENRES),
        'total_users': 1234,
    }
    return render(request, 'pages/books_by_year.html', context)