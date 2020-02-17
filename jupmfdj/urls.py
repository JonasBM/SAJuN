from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from django.urls import path
from django.views.generic import RedirectView

urlpatterns = [
                path('admin/', admin.site.urls),
                path('', include('juapp.urls')),
                path('accounts/', include('django.contrib.auth.urls')),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)