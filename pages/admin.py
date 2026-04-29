from django.contrib import admin

from django.contrib import admin
from .models import Book, Category, TagPost
from django.contrib import messages

class RatingFilter(admin.SimpleListFilter):
    title = 'Рейтинг'
    parameter_name = 'rating'

    def lookups(self, request, model_admin):
        return [
            ('high', 'Высокий (4.5 и выше)'),
            ('medium', 'Средний (3.0 - 4.4)'),
            ('low', 'Низкий (ниже 3.0)'),
        ]

    def queryset(self, request, queryset):
        if self.value() == 'high':
            return queryset.filter(rating__gte=4.5)
        if self.value() == 'medium':
            return queryset.filter(rating__gte=3.0, rating__lt=4.5)
        if self.value() == 'low':
            return queryset.filter(rating__lt=3.0)
        return queryset

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'slug')
    list_display_links = ('id', 'name')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}
    ordering = ('name',)


@admin.register(TagPost)
class TagPostAdmin(admin.ModelAdmin):
    list_display = ('id', 'tag', 'slug')
    list_display_links = ('id', 'tag')
    search_fields = ('tag',)
    prepopulated_fields = {'slug': ('tag',)}
    ordering = ('tag',)


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'year', 'rating', 'cat', 'is_published', 'short_content', 'book_info')
    list_display_links = ('title',)
    list_editable = ('rating', 'is_published')
    list_filter = ('cat', 'is_published', 'year', RatingFilter)
    search_fields = ('title', 'author', 'cat__name')
    ordering = ('-time_create',)
    list_per_page = 10
    filter_horizontal = ('tags',)
    actions = ['make_published', 'make_draft']
    fields = ('title', 'slug', 'author', 'content', 'year', 'rating', 'cat', 'tags', 'is_published', 'time_create', 'time_update')
    readonly_fields = ('time_create', 'time_update')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('tags',)

    @admin.display(description="Краткое содержание")
    def short_content(self, book: Book):
        if len(book.content) > 100:
            return f"{book.content[:100]}..."
        return book.content

    @admin.display(description="Информация о книге", ordering='title')
    def book_info(self, book: Book):
        return f"{book.title} ({book.year}) - {book.author}"

    @admin.action(description="Опубликовать выбранные книги")
    def make_published(self, request, queryset):
        count = queryset.update(is_published=Book.Status.PUBLISHED)
        self.message_user(request, f"Опубликовано {count} книг(и).")

    @admin.action(description="Снять с публикации выбранные книги")
    def make_draft(self, request, queryset):
        count = queryset.update(is_published=Book.Status.DRAFT)
        self.message_user(request, f"{count} книг(и) сняты с публикации.", messages.WARNING)

