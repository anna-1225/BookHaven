from django.contrib import admin
from django.urls import path, include
from pages import views as pages_vie
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

from django.conf import settings
from django.conf.urls.static import static

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)