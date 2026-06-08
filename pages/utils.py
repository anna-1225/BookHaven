from .models import Category, TagPost, Book
from django.db.models import Count

menu = [
    {'title': 'Главная', 'url_name': 'home'},
    {'title': 'Жанры', 'url_name': 'genres'},
]


class DataMixin:
    paginate_by = 6
    title_page = None
    extra_context = {}

    def __init__(self):
        if self.title_page:
            self.extra_context['title'] = self.title_page
        if 'categories' not in self.extra_context:
            self.extra_context['categories'] = Category.objects.all()
        if 'tags' not in self.extra_context:
            self.extra_context['tags'] = TagPost.objects.all()
        if 'online_users' not in self.extra_context:
            self.extra_context['online_users'] = 42
        if 'total_users' not in self.extra_context:
            self.extra_context['total_users'] = 1234
        if 'total_books' not in self.extra_context:
            self.extra_context['total_books'] = Book.published.count()
        self.extra_context['selected_category'] = 0

    def get_mixin_context(self, context, **kwargs):
        popular_genre = Category.objects.annotate(
            book_count=Count('books')
        ).order_by('-book_count').first()

        context['categories'] = Category.objects.all()
        context['tags'] = TagPost.objects.all()
        context['online_users'] = 42
        context['total_users'] = 1234
        context['total_books'] = Book.published.count()
        context['popular_genre'] = popular_genre.name if popular_genre else 'Нет данных'
        context['popular_genre_count'] = popular_genre.book_count if popular_genre else 0
        context['selected_category'] = 0
        context.update(kwargs)
        return context