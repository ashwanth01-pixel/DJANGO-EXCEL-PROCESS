from django.contrib import admin
from django.urls import path
from excelapp import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('upload/', views.upload_file, name='upload_file'),
    path('summary/', views.summary, name='summary'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)