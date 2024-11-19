from django.urls import path 
from django.conf import settings
from django.conf.urls.static import static

from .views import (
    convert,
)


urlpatterns = [
    path('convert/', convert, name='convert')
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
