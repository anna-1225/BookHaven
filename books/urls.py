from django.urls import path, register_converter
from . import views
from . import converters

register_converter(converters.YearConverter, 'year')

urlpatterns = [
    path('', views.index, name='home'),
    path('genres/', views.genres_list, name='genres'),
    path('genre/<slug:genre_slug>/', views.genre_detail, name='genre_detail'),
    path('book/<slug:book_slug>/', views.book_detail, name='book_detail'),  # только slug!
    path('year/<year:pub_year>/', views.books_by_year, name='books_by_year'),
    path('old-catalog/', views.old_catalog_redirect, name='old_catalog'),
]