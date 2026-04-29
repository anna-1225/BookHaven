from django.contrib import admin
from django.urls import path, include
from pages import views as pages_views

admin.site.site_header = "Панель управления BookHaven"
admin.site.site_title = "BookHaven Администрирование"
admin.site.index_title = "Добро пожаловать в панель управления книжным форумом"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('books.urls')),
]

handler404 = pages_views.error_404
handler500 = pages_views.error_500