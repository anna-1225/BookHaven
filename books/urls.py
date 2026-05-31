from django.urls import path, register_converter
from . import views
from . import converters

register_converter(converters.YearConverter, 'year')

urlpatterns = [
    path('', views.BookHome.as_view(), name='home'),

    path('genres/', views.genres_list, name='genres'),
    path('genre/<slug:genre_slug>/', views.genre_detail, name='genre_detail'),
    path('category/<slug:cat_slug>/', views.BookCategory.as_view(), name='category'),

    path('book/<slug:book_slug>/', views.ShowBook.as_view(), name='book_detail'),
    path('year/<year:pub_year>/', views.books_by_year, name='books_by_year'),
    path('all-books/', views.AllBooks.as_view(), name='all_books'),

    path('tag/<slug:tag_slug>/', views.BookTag.as_view(), name='tag'),

    path('add-book/', views.AddBook.as_view(), name='add_book'),
    path('add-book-model/', views.CreateBook.as_view(), name='add_book_model'),
    path('edit/<slug:slug>/', views.UpdateBook.as_view(), name='edit_book'),
    path('delete/<slug:slug>/', views.DeleteBook.as_view(), name='delete_book'),
    path('upload/', views.upload_file, name='upload_file'),

    path('old-catalog/', views.old_catalog_redirect, name='old_catalog'),
    path('about/', views.AboutView.as_view(), name='about'),
]