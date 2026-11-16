import os

from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_GET

from academics.junior_content import JUNIOR_SLUG
from academics.models import Programme
from gallery.models import Photo
from news.models import Event, Post

from .emails import notify_school, send_templated
from .forms import ContactForm
from .models import FAQ, Feature, StaffMember, Testimonial


def home(request):
    return render(request, "core/home.html", {
        "features": Feature.objects.all()[:6],
        "programmes": Programme.objects.filter(is_active=True).exclude(slug=JUNIOR_SLUG)[:4],
        "junior": Programme.objects.filter(is_active=True, slug=JUNIOR_SLUG).first(),
        "posts": Post.objects.published()[:3],
        "events": Event.objects.filter(date__gte=timezone.localdate())[:3],
        "photos": Photo.objects.filter(album__is_published=True).select_related("album")[:8],
        "testimonials": Testimonial.objects.filter(is_published=True)[:6],
    })


def about(request):
    return render(request, "core/about.html", {
        "staff": StaffMember.objects.filter(is_active=True),
        "features": Feature.objects.all(),
    })


def contact(request):
    form = ContactForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        msg = form.save()
        ctx = {"m": msg, "admin_url": settings.SITE_URL + reverse(
            "admin:core_contactmessage_change", args=[msg.pk])}
        notify_school(f"Website enquiry: {msg.subject}", "contact_school", ctx, reply_to=msg.email)
        send_templated("We received your message — Little Harvard ECD Centre",
                       "contact_ack", ctx, [msg.email])
        messages.success(request, "Thank you! Your message has been sent. We'll get back to you soon.")
        return redirect("core:contact")
    return render(request, "core/contact.html", {"form": form, "faqs": FAQ.objects.all()})


@require_GET
def robots_txt(request):
    lines = ["User-agent: *", "Disallow: /admin/", f"Sitemap: {settings.SITE_URL}/sitemap.xml"]
    return HttpResponse("\n".join(lines), content_type="text/plain")


@require_GET
def healthz(request):
    """Deployment diagnostics: reports which pieces are configured, never their values."""
    from django.db import connection
    from django.db.migrations.executor import MigrationExecutor

    db = {"engine": connection.vendor, "database_url_set": bool(os.environ.get("DATABASE_URL"))}
    try:
        connection.ensure_connection()
        executor = MigrationExecutor(connection)
        pending = executor.migration_plan(executor.loader.graph.leaf_nodes())
        db.update(connected=True, pending_migrations=len(pending))
    except Exception as exc:
        db.update(connected=False, error=type(exc).__name__)
    checks = {
        "database": db,
        "debug": settings.DEBUG,
        "secret_key_set": bool(os.environ.get("SECRET_KEY")),
        "site_url": settings.SITE_URL,
        "media_storage": "backblaze-b2" if settings.B2_BUCKET else "local-disk (read-only on Vercel)",
        "email_configured": bool(settings.EMAIL_HOST_USER and settings.EMAIL_HOST_PASSWORD),
        "google_analytics": bool(settings.GA_MEASUREMENT_ID),
    }
    if settings.B2_BUCKET:
        from django.core.files.storage import default_storage
        try:
            default_storage.connection.meta.client.head_bucket(Bucket=settings.B2_BUCKET)
            checks["media_storage_connected"] = True
        except Exception as exc:
            checks["media_storage_connected"] = False
            checks["media_storage_error"] = type(exc).__name__
            if isinstance(exc, ValueError):  # boto config errors, e.g. bad endpoint; no secrets
                checks["media_storage_detail"] = str(exc)[:200]
            checks["media_storage_endpoint"] = settings.AWS_S3_ENDPOINT_URL
            checks["media_storage_region"] = settings.AWS_S3_REGION_NAME
    ok = db.get("connected") and db.get("pending_migrations") == 0
    return JsonResponse({"ok": bool(ok), **checks}, status=200 if ok else 503)


def page_not_found(request, exception):
    return render(request, "404.html", status=404)
