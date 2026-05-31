from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy

from pages.models import Book, Category, TagPost
from pages.forms import AddBookForm, BookModelForm, UploadFileForm
from pages.utils import DataMixin


GENRES = [
    {'id': 1, 'name': 'Фэнтези', 'slug': 'fantasy', 'book_count': 45},
    {'id': 2, 'name': 'Детектив', 'slug': 'detective', 'book_count': 32},
    {'id': 3, 'name': 'Классика', 'slug': 'classic', 'book_count': 28},
    {'id': 4, 'name': 'Роман', 'slug': 'romance', 'book_count': 37},
]


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


class AllBooks(DataMixin, ListView):
    model = Book
    template_name = 'pages/all_books.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        return Book.published.all().select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Все книги'
        context['selected_category'] = 0
        context['total_books'] = Book.published.count()
        return context


def old_catalog_redirect(request):
    return redirect('genres')


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']
            import os
            from django.conf import settings
            import uuid
            ext = os.path.splitext(uploaded_file.name)[1]
            unique_name = f"{uuid.uuid4().hex}{ext}"
            upload_dir = os.path.join(settings.MEDIA_ROOT, 'uploads')
            os.makedirs(upload_dir, exist_ok=True)
            file_path = os.path.join(upload_dir, unique_name)
            with open(file_path, 'wb+') as destination:
                for chunk in uploaded_file.chunks():
                    destination.write(chunk)
            return render(request, 'pages/upload_success.html', {'file_name': uploaded_file.name})
    else:
        form = UploadFileForm()
    return render(request, 'pages/upload_file.html', {'form': form, 'title': 'Загрузка файла'})


class BookHome(DataMixin, ListView):
    model = Book
    template_name = 'pages/index.html'
    context_object_name = 'posts'
    paginate_by = 6

    def get_queryset(self):
        return Book.published.all().select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Главная страница книжного форума BookHaven'
        context['selected_category'] = 0
        context['total_books'] = Book.published.count()
        return context


class BookCategory(DataMixin, ListView):
    model = Book
    template_name = 'pages/index.html'
    context_object_name = 'posts'
    allow_empty = False
    paginate_by = 6

    def get_queryset(self):
        return Book.published.filter(cat__slug=self.kwargs['cat_slug']).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        category = Category.objects.get(slug=self.kwargs['cat_slug'])
        context['title'] = f'Книги жанра: {category.name}'
        context['selected_category'] = category.pk
        return context


class BookTag(DataMixin, ListView):
    model = Book
    template_name = 'pages/index.html'
    context_object_name = 'posts'
    allow_empty = False
    paginate_by = 6

    def get_queryset(self):
        return Book.published.filter(tags__slug=self.kwargs['tag_slug']).select_related('cat')

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        tag = TagPost.objects.get(slug=self.kwargs['tag_slug'])
        context['title'] = f'Тег: {tag.tag}'
        context['selected_category'] = 0
        return context


class ShowBook(DataMixin, DetailView):
    model = Book
    template_name = 'pages/book_detail.html'
    context_object_name = 'book'
    slug_url_kwarg = 'book_slug'

    def get_object(self, queryset=None):
        return get_object_or_404(Book.published, slug=self.kwargs[self.slug_url_kwarg])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.title
        context['genre_name'] = self.object.genre
        context['comments'] = [
            {'id': 1, 'author': 'BookLover', 'date': '2026-01-15 14:30',
             'text': 'Отличная книга! Очень понравилось обсуждение на форуме.', 'likes': 5},
            {'id': 2, 'author': 'Reader123', 'date': '2026-01-16 09:45',
             'text': 'Очень понравилось обсуждение.', 'likes': 3},
            {'id': 3, 'author': 'BookWorm', 'date': '2026-01-16 18:20',
             'text': 'Жду продолжения!', 'likes': 2},
        ]
        return context


class AddBook(DataMixin, FormView):
    form_class = AddBookForm
    template_name = 'pages/add_book.html'
    success_url = reverse_lazy('home')
    title_page = 'Добавление книги (несвязанная форма)'

    def form_valid(self, form):
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
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавление книги (несвязанная форма)'
        return context


class CreateBook(DataMixin, CreateView):
    model = Book
    fields = ['title', 'slug', 'author', 'content', 'year', 'rating', 'is_published', 'cat', 'tags', 'photo']
    template_name = 'pages/add_book.html'
    success_url = reverse_lazy('home')
    title_page = 'Добавление книги'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Добавление книги'
        return context


class UpdateBook(DataMixin, UpdateView):
    model = Book
    fields = ['title', 'slug', 'author', 'content', 'year', 'rating', 'is_published', 'cat', 'tags', 'photo']
    template_name = 'pages/add_book.html'
    success_url = reverse_lazy('home')
    title_page = 'Редактирование книги'
    slug_url_kwarg = 'slug'

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование книги'
        return context


class DeleteBook(DataMixin, DeleteView):
    model = Book
    template_name = 'pages/confirm_delete.html'
    success_url = reverse_lazy('home')
    title_page = 'Удаление книги'
    slug_url_kwarg = 'slug'
from django.views.generic import TemplateView


class AboutView(TemplateView):
    template_name = 'pages/about.html'
    extra_context = {
        'title': 'О сайте',
    }