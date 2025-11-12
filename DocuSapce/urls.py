from django.contrib import admin
from django.urls import path, include  # <- include doit être importé !

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('files.urls')),  # <- Assure-toi que c'est exactement ça
]

from django.conf import settings
from django.conf.urls.static import static

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
