from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include
from django.urls import path
from django.views.generic import RedirectView

urlpatterns = [
                path('admin/', admin.site.urls),
                # path('juapp/', include('juapp.urls')),
                # path('', RedirectView.as_view(url='juapp/')),
                path('', include('juapp.urls')),
                path('accounts/', include('django.contrib.auth.urls')),
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

print(static(settings.STATIC_URL, document_root=settings.STATIC_ROOT))