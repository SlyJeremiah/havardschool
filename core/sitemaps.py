from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from academics.models import Programme
from gallery.models import Album
from news.models import Event, Post


class StaticSitemap(Sitemap):
    changefreq = "monthly"
    priority = 0.8

    def items(self):
        return ["core:home", "core:about", "core:contact", "academics:list",
                "admissions:index", "admissions:apply", "news:list", "news:events", "gallery:list"]

    def location(self, item):
        return reverse(item)


class ProgrammeSitemap(Sitemap):
    changefreq = "monthly"

    def items(self):
        return Programme.objects.filter(is_active=True)


class PostSitemap(Sitemap):
    changefreq = "weekly"

    def items(self):
        return Post.objects.published()

    def lastmod(self, obj):
        return obj.updated_at


class EventSitemap(Sitemap):
    def items(self):
        return Event.objects.all()


class AlbumSitemap(Sitemap):
    def items(self):
        return Album.objects.filter(is_published=True)


sitemaps = {
    "static": StaticSitemap,
    "programmes": ProgrammeSitemap,
    "news": PostSitemap,
    "events": EventSitemap,
    "gallery": AlbumSitemap,
}
