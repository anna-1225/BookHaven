from django.urls import path, register_converter
from . import views
from . import converters

register_converter(converters.YearConverter, 'year')

urlpatterns = [
    path('', views.index, name='home'),
    path('genres/', views.genres_list, name='genres'),
    path('genre/<slug:genre_slug>/', views.genre_detail, name='genre_detail'),
    path('genre/<slug:genre_slug>/<int:book_id>/', views.book_detail, name='book_detail'),
    path('year/<year:pub_year>/', views.books_by_year, name='books_by_year'),
    path('old-catalog/', views.old_catalog_redirect, name='old_catalog'),
]