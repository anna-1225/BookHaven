from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from pages.models import Book, Category, TagPost
from pages.forms import AddBookForm, BookModelForm, UploadFileForm
import uuid
import os
from django.conf import settings


GENRES = [
    {'id': 1, 'name': 'Фэнтези', 'slug': 'fantasy', 'book_count': 45},
    {'id': 2, 'name': 'Детектив', 'slug': 'detective', 'book_count': 32},
    {'id': 3, 'name': 'Классика', 'slug': 'classic', 'book_count': 28},
    {'id': 4, 'name': 'Роман', 'slug': 'romance', 'book_count': 37},
]


def index(request):
    books = Book.published.all()[:3]
    categories = Category.objects.all()
    tags = TagPost.objects.all()
    total_books = Book.published.count()

    context = {
        'title': 'Главная страница книжного форума BookHaven',
        'posts': books,
        'categories': categories,
        'tags': tags,
        'online_users': 42,
        'selected_category': 0,
        'total_books': total_books,
        'total_users': 1234,
    }
    return render(request, 'pages/index.html', context)


def genres_list(request):
    total_books = Book.published.count()
    categories = Category.objects.all()
    tags = TagPost.objects.all()

    context = {
        'title': 'Литературные жанры',
        'genres': GENRES,
        'categories': categories,
        'tags': tags,
        'online_users': 42,
        'selected_category': 0,
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
    categories = Category.objects.all()
    tags = TagPost.objects.all()

    context = {
        'title': f'Книги жанра {genre["name"]}',
        'genre_name': genre['name'],
        'genre_slug': genre_slug,
        'books': books,
        'genres': GENRES,
        'categories': categories,
        'tags': tags,
        'online_users': 42,
        'selected_category': genre['id'],
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
    categories = Category.objects.all()
    tags = TagPost.objects.all()

    context = {
        'title': f'{book.title}',
        'genre_name': genre['name'] if genre else book.genre,
        'book': book,
        'comments': filtered_comments,
        'genres': GENRES,
        'categories': categories,
        'tags': tags,
        'online_users': 42,
        'selected_category': genre['id'] if genre else 0,
        'total_books': total_books,
        'total_users': 1234,
    }
    return render(request, 'pages/book_detail.html', context)


def show_category(request, cat_slug):
    category = get_object_or_404(Category, slug=cat_slug)
    books = Book.published.filter(cat=category)
    categories = Category.objects.all()
    tags = TagPost.objects.all()
    total_books = Book.published.count()

    context = {
        'title': f'Книги жанра: {category.name}',
        'posts': books,
        'categories': categories,
        'tags': tags,
        'selected_category': category.pk,
        'total_books': total_books,
        'total_users': 1234,
        'online_users': 42,
    }
    return render(request, 'pages/index.html', context)


def show_tag(request, tag_slug):
    tag = get_object_or_404(TagPost, slug=tag_slug)
    books = tag.books.filter(is_published=Book.Status.PUBLISHED)
    categories = Category.objects.all()
    tags = TagPost.objects.all()
    total_books = Book.published.count()

    context = {
        'title': f'Тег: {tag.tag}',
        'posts': books,
        'categories': categories,
        'tags': tags,
        'selected_category': 0,
        'total_books': total_books,
        'total_users': 1234,
        'online_users': 42,
    }
    return render(request, 'pages/index.html', context)


def books_by_year(request, pub_year):
    if pub_year <= 0:
        return redirect('home')

    books_in_year = Book.published.filter(year=pub_year)
    total_books = Book.published.count()
    categories = Category.objects.all()
    tags = TagPost.objects.all()

    context = {
        'title': f'Книги {pub_year} года',
        'pub_year': pub_year,
        'books': books_in_year,
        'genres': GENRES,
        'categories': categories,
        'tags': tags,
        'online_users': 42,
        'selected_category': 0,
        'total_books': total_books,
        'total_users': 1234,
    }
    return render(request, 'pages/books_by_year.html', context)


def old_catalog_redirect(request):
    return redirect('genres')


def add_book(request):
    if request.method == 'POST':
        form = AddBookForm(request.POST)
        if form.is_valid():
            try:
                Book.objects.create(
                    title=form.cleaned_data['title'],
                    slug=form.cleaned_data['slug'],
                    author=form.cleaned_data['author'],
                    content=form.cleaned_data['content'],
                    year=form.cleaned_data['year'],
                    rating=form.cleaned_data['rating'] or 0,
                    is_published=form.cleaned_data['is_published'],
                    cat=form.cleaned_data['cat']
                )
                return redirect('home')
            except Exception as e:
                form.add_error(None, f'Ошибка: {str(e)}')
    else:
        form = AddBookForm()
    return render(request, 'pages/add_book.html', {'form': form, 'title': 'Добавление книги'})


def add_book_model(request):
    if request.method == 'POST':
        form = BookModelForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = BookModelForm()

    return render(request, 'pages/add_book.html', {
        'title': 'Добавление книги',
        'form': form
    })


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']
            import os
            from django.conf import settings
            upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
            os.makedirs(upload_dir, exist_ok=True)
            file_path = os.path.join(upload_dir, uploaded_file.name)
            with open(file_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)
            return render(request, 'pages/upload_success.html', {'file_name': uploaded_file.name})
    else:
        form = UploadFileForm()
    return render(request, 'pages/upload_file.html', {'form': form, 'title': 'Загрузка файла'})

def all_books(request):
    books = Book.published.all()
    categories = Category.objects.all()
    tags = TagPost.objects.all()
    total_books = books.count()

    context = {
        'title': 'Все книги',
        'posts': books,
        'categories': categories,
        'tags': tags,
        'online_users': 42,
        'selected_category': 0,
        'total_books': total_books,
        'total_users': 1234,
    }
    return render(request, 'pages/all_books.html', context)


def handle_uploaded_file(f):
    ext = os.path.splitext(f.name)[1]
    unique_name = f"{uuid.uuid4().hex}{ext}"
    file_path = os.path.join(settings.MEDIA_ROOT, 'uploads', unique_name)
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)

    return f"uploads/{unique_name}"


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            file_path = handle_uploaded_file(request.FILES['file'])
            return render(request, 'pages/upload_success.html', {
                'file_path': file_path,
                'file_name': request.FILES['file'].name
            })
    else:
        form = UploadFileForm()

    return render(request, 'pages/upload_file.html', {
        'title': 'Загрузка файла',
        'form': form
    })
