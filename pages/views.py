from django.http import HttpResponse

def error_404(request, exception):
    return HttpResponse("Ошибка 404: запрошенная страница не найдена", status=404)


def error_500(request):
    return HttpResponse("Ошибка 500: внутренняя ошибка сервера", status=500)