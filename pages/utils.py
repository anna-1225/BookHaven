from .models import Category, TagPost

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
        self.extra_context['selected_category'] = 0

    def get_mixin_context(self, context, **kwargs):
        context['categories'] = Category.objects.all()
        context['tags'] = TagPost.objects.all()
        context['online_users'] = 42
        context['total_users'] = 1234
        context['selected_category'] = 0
        context.update(kwargs)
        return context