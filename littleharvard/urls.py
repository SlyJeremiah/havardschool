from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.sitemaps.views import sitemap
from django.urls import include, path

from core.sitemaps import sitemaps
from core.views import healthz, robots_txt

admin.site.site_header = "Little Harvard ECD Centre"
admin.site.site_title = "Little Harvard Admin"
admin.site.index_title = "Website management"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("sitemap.xml", sitemap, {"sitemaps": sitemaps}, name="sitemap"),
    path("robots.txt", robots_txt, name="robots_txt"),
    path("healthz/", healthz, name="healthz"),
    path("programmes/", include("academics.urls")),
    path("admissions/", include("admissions.urls")),
    path("news/", include("news.urls")),
    path("gallery/", include("gallery.urls")),
    path("", include("core.urls")),
]

if settings.DEBUG and not getattr(settings, "B2_BUCKET", None):
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = "core.views.page_not_found"
