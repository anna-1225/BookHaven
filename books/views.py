from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.db.models import Count
from django.utils.text import slugify

from pages.models import Book, Category, TagPost, Comment, CommentLike
from pages.forms import AddBookForm, BookModelForm, UploadFileForm
from pages.utils import DataMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from .mixins import AuthorRequiredMixin
from django.views.generic import TemplateView
from django.contrib.auth.decorators import login_required


def genres_list(request):
    categories_with_count = Category.objects.annotate(
        book_count=Count('books')
    ).filter(book_count__gt=0)

    total_books = Book.published.count()
    categories = Category.objects.all()
    tags = TagPost.objects.all()

    context = {
        'title': 'Литературные жанры',
        'genres': categories_with_count,
        'categories': categories,
        'tags': tags,
        'online_users': 42,
        'selected_category': 0,
        'total_books': total_books,
        'total_users': 1234,
    }
    return render(request, 'pages/genres.html', context)


def genre_detail(request, genre_slug):
    category = get_object_or_404(Category, slug=genre_slug)

    books = Book.published.filter(cat=category)

    total_books = Book.published.count()
    categories = Category.objects.all()
    tags = TagPost.objects.all()

    context = {
        'title': f'Книги жанра {category.name}',
        'genre_name': category.name,
        'genre_slug': genre_slug,
        'books': books,
        'categories': categories,
        'tags': tags,
        'online_users': 42,
        'selected_category': category.id,
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
        return self.get_mixin_context(context,
                                      title='Все книги',
                                      selected_category=0
                                      )


def old_catalog_redirect(request):
    return redirect('genres')


@login_required
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
        return self.get_mixin_context(context,
                                      title='Главная страница книжного форума BookHaven',
                                      selected_category=0
                                      )


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
        return self.get_mixin_context(context,
                                      title=f'Книги жанра: {category.name}',
                                      selected_category=category.pk
                                      )


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
        return self.get_mixin_context(context,
                                      title=f'Тег: {tag.tag}',
                                      selected_category=0
                                      )


class ShowBook(DataMixin, DetailView):
    model = Book
    template_name = 'pages/book_detail.html'
    context_object_name = 'book'
    slug_url_kwarg = 'book_slug'

    def get_object(self, queryset=None):
        return get_object_or_404(Book.published, slug=self.kwargs[self.slug_url_kwarg])

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.object.cat:
            genre_name = self.object.cat.name
        else:
            genre_name = 'Не указан'

        return self.get_mixin_context(context,
                                      title=self.object.title,
                                      genre_name=genre_name,
                                      user=self.request.user,
                                      comments=self.object.comments.all()
                                      )


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
        return self.get_mixin_context(context,
                                      title='Добавление книги (несвязанная форма)'
                                      )


class CreateBook(LoginRequiredMixin, DataMixin, CreateView):
    model = Book
    fields = ['title', 'slug', 'author', 'content', 'year', 'rating', 'is_published', 'cat', 'tags', 'photo']
    template_name = 'pages/add_book.html'
    success_url = reverse_lazy('home')
    title_page = 'Добавление книги'

    def form_valid(self, form):
        book = form.save(commit=False)
        book.author_user = self.request.user

        if not book.slug or book.slug == '':
            base_slug = slugify(book.title)
            book.slug = base_slug
        else:
            base_slug = book.slug

        counter = 1
        while Book.objects.filter(slug=book.slug).exclude(id=book.id).exists():
            book.slug = f"{base_slug}-{counter}"
            counter += 1

        book.save()
        form.save_m2m()
        return redirect(self.success_url)

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        return self.get_mixin_context(context,
                                      title='Добавление книги'
                                      )


class UpdateBook(AuthorRequiredMixin, LoginRequiredMixin, DataMixin, UpdateView):
    model = Book
    fields = ['title', 'slug', 'author', 'content', 'year', 'rating', 'is_published', 'cat', 'tags', 'photo']
    template_name = 'pages/add_book.html'
    success_url = reverse_lazy('home')
    title_page = 'Редактирование книги'
    slug_url_kwarg = 'slug'


class DeleteBook(AuthorRequiredMixin, LoginRequiredMixin, DataMixin, DeleteView):
    model = Book
    template_name = 'pages/confirm_delete.html'
    success_url = reverse_lazy('home')
    title_page = 'Удаление книги'
    slug_url_kwarg = 'slug'


class AboutView(TemplateView):
    template_name = 'pages/about.html'
    extra_context = {
        'title': 'О сайте',
    }


@login_required
def add_comment(request, book_slug):
    book = get_object_or_404(Book, slug=book_slug)
    if request.method == 'POST':
        text = request.POST.get('text')
        if text:
            Comment.objects.create(
                book=book,
                author=request.user,
                text=text
            )
    return redirect('book_detail', book_slug=book_slug)


@login_required
def like_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    like, created = CommentLike.objects.get_or_create(
        comment=comment,
        user=request.user
    )

    if created:
        comment.likes_count += 1
        comment.save()
    else:
        like.delete()
        comment.likes_count -= 1
        comment.save()

    return redirect(request.META.get('HTTP_REFERER', 'home'))

class RulesView(TemplateView):
    template_name = 'pages/rules.html'
    extra_context = {
        'title': 'Правила форума',
    }


class HelpView(TemplateView):
    template_name = 'pages/help.html'
    extra_context = {
        'title': 'Помощь',
    }


class ContactsView(TemplateView):
    template_name = 'pages/contacts.html'
    extra_context = {
        'title': 'Контакты',
    }