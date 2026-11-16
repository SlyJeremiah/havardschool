"""Branded admin site with a content-management dashboard as its home page."""
from django.conf import settings
from django.contrib import admin
from django.urls import NoReverseMatch, reverse
from django.utils import timezone


class LittleHarvardAdminSite(admin.AdminSite):
    site_header = "Little Harvard ECD Centre"
    site_title = "Little Harvard Admin"
    index_title = "Content management"
    index_template = "admin/dashboard.html"

    def index(self, request, extra_context=None):
        return super().index(request, {**self._dashboard(request), **(extra_context or {})})

    # -- helpers ---------------------------------------------------------------
    def _can(self, request, model, action="view"):
        ma = self._registry.get(model)
        if ma is None:
            return False
        return getattr(ma, f"has_{action}_permission")(request)

    @staticmethod
    def _url(name, *args, query=""):
        try:
            return reverse(f"admin:{name}", args=args) + query
        except NoReverseMatch:
            return ""

    def _dashboard(self, request):
        from academics.models import Programme
        from admissions.models import Application
        from gallery.models import Album, Photo, Video
        from news.models import Event, Post

        from .models import ContactMessage, SiteSettings

        today = timezone.localdate()
        can = lambda m, a="view": self._can(request, m, a)  # noqa: E731

        stats, actions = [], []
        if can(Application):
            new_apps = Application.objects.filter(status="new").count()
            stats.append(dict(label="New applications", value=new_apps, icon="bi-person-plus",
                              tone="orange" if new_apps else "muted",
                              url=self._url("admissions_application_changelist", query="?status__exact=new")))
        if can(ContactMessage):
            unread = ContactMessage.objects.filter(is_handled=False).count()
            stats.append(dict(label="Unanswered messages", value=unread, icon="bi-envelope",
                              tone="orange" if unread else "muted",
                              url=self._url("core_contactmessage_changelist", query="?is_handled__exact=0")))
        if can(Event):
            stats.append(dict(label="Upcoming events", value=Event.objects.filter(date__gte=today).count(),
                              icon="bi-calendar-event", tone="green",
                              url=self._url("news_event_changelist")))
        if can(Post):
            stats.append(dict(label="Published news posts", value=Post.objects.published().count(),
                              icon="bi-newspaper", tone="navy", url=self._url("news_post_changelist")))
        if can(Album):
            stats.append(dict(label="Gallery photos", value=Photo.objects.count(), icon="bi-images",
                              tone="yellow", url=self._url("gallery_album_changelist")))

        quick = [
            (Post, "add", "Write a news post", "bi-pencil-square", "news_post_add"),
            (Event, "add", "Add an event", "bi-calendar-plus", "news_event_add"),
            (Album, "add", "Upload photos", "bi-cloud-arrow-up", "gallery_album_add"),
            (Video, "add", "Add a video / reel", "bi-play-btn", "gallery_video_add"),
            (SiteSettings, "change", "Edit school info & banner", "bi-sliders", "core_sitesettings_changelist"),
            (Programme, "change", "Edit programmes & fees", "bi-mortarboard", "academics_programme_changelist"),
        ]
        for model, perm, label, icon, name in quick:
            if can(model, perm):
                actions.append(dict(label=label, icon=icon, url=self._url(name)))

        recent_apps = (Application.objects.select_related("programme")[:6] if can(Application) else None)
        recent_msgs = (ContactMessage.objects.all()[:6] if can(ContactMessage) else None)

        setup = []
        if request.user.is_superuser:
            setup = [
                dict(label="Email notifications", ok=bool(settings.EMAIL_HOST_USER and settings.EMAIL_HOST_PASSWORD),
                     hint="Set EMAIL_HOST_USER / EMAIL_HOST_PASSWORD in Vercel"),
                dict(label="Google Analytics", ok=bool(settings.GA_MEASUREMENT_ID),
                     hint="Set GA_MEASUREMENT_ID in Vercel"),
                dict(label="Photo storage (Backblaze B2)", ok=bool(settings.B2_BUCKET),
                     hint="Set the B2_* variables in Vercel"),
                dict(label="Admissions open", ok=SiteSettings.load().admissions_open,
                     hint="Turn on in Site settings"),
            ]

        return {
            "dash_stats": stats,
            "dash_actions": actions,
            "dash_recent_apps": recent_apps,
            "dash_recent_msgs": recent_msgs,
            "dash_setup": setup,
        }

