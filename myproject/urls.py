from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView  # 👈 Import this to use TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),  # Default Django admin
    path('admin-panel/', include('myapp.admin_urls', namespace='custom_admin')),  # Renamed namespace
    path('', include('myapp.urls')),  # User-facing URLs

    # ✅ Zoho domain verification route
    path(
        "zoho-domain-verification.html",
        TemplateView.as_view(template_name="zoho-domain-verification.html"),
        name="zoho_verify"
    ),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
