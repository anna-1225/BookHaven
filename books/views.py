from django.http import HttpResponse, Http404
from django.shortcuts import redirect


def index(request):
    return HttpResponse("Главная страница книжного форума BookHaven")


def genres_list(request):
    return HttpResponse("Страница со списком литературных жанров")


def genre_detail(request, genre_slug):
    valid_genres = ['fantasy', 'detective', 'classic', 'romance']
    if genre_slug not in valid_genres:
        raise Http404("Жанр не найден")

    return HttpResponse(f"Страница жанра {genre_slug}")


def book_detail(request, genre_slug, book_id):
    if int(book_id) > 10:
        raise Http404("Книга не найдена")

    comment_id = request.GET.get('comment_id', '')

    print(f"[DEBUG] GET-параметр comment_id = {comment_id}")
    print(f"[DEBUG] Все GET-параметры: {request.GET}")

    return HttpResponse(f"Страница книги с ID {book_id} в жанре {genre_slug}")


def old_catalog_redirect(request):
    return redirect('genres')

def books_by_year(request, pub_year):
    if pub_year <= 0:
        return redirect('home')
    return HttpResponse(f"Книги, изданные в {pub_year} году")