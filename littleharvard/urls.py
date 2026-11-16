from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.templatetags.static import static as static_url
from django.urls import include, path
from django.views.generic import RedirectView

from core.sitemaps import sitemaps
from core.views import healthz, robots_txt

urlpatterns = [
    path("admin/", admin.site.urls),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
    path("robots.txt", robots_txt, name="robots_txt"),
    path("healthz/", healthz, name="healthz"),
    path("favicon.ico", RedirectView.as_view(url=static_url("favicon.ico"), permanent=True)),
    path("programmes/", include("academics.urls")),
    path("admissions/", include("admissions.urls")),
    path("news/", include("news.urls")),
    path("gallery/", include("gallery.urls")),
    path("", include("core.urls")),
]

if settings.DEBUG and not getattr(settings, "B2_BUCKET", None):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = "core.views.page_not_found"
