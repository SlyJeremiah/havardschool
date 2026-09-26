from django.conf import settings
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_GET

from academics.models import Programme
from gallery.models import Photo
from news.models import Event, Post

from .emails import notify_school, send_templated
from .forms import ContactForm
from .models import FAQ, Feature, StaffMember, Testimonial


def home(request):
    return render(request, "core/home.html", {
        "features": Feature.objects.all()[:6],
        "programmes": Programme.objects.filter(is_active=True)[:4],
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


def page_not_found(request, exception):
    return render(request, "404.html", status=404)
