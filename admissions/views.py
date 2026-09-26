from django.conf import settings
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from academics.models import Programme
from core.emails import notify_school, send_templated
from core.models import FAQ

from .forms import ApplicationForm
from .models import AdmissionStep, Application, Requirement


def index(request):
    return render(request, "admissions/index.html", {
        "steps": AdmissionStep.objects.all(),
        "requirements": Requirement.objects.all(),
        "programmes": Programme.objects.filter(is_active=True),
        "faqs": FAQ.objects.all(),
    })


def apply(request):
    initial = {}
    if slug := request.GET.get("programme"):
        initial["programme"] = Programme.objects.filter(slug=slug).first()
    form = ApplicationForm(request.POST or None, initial=initial)
    if request.method == "POST" and form.is_valid():
        app = form.save()
        ctx = {"a": app, "admin_url": settings.SITE_URL + reverse(
            "admin:admissions_application_change", args=[app.pk])}
        notify_school(f"New application {app.reference}: {app.child_name}",
                      "application_school", ctx, reply_to=app.parent_email)
        send_templated(f"Application received ({app.reference}) — Little Harvard ECD Centre",
                       "application_ack", ctx, [app.parent_email])
        request.session["last_application"] = app.reference
        return redirect("admissions:thanks", reference=app.reference)
    return render(request, "admissions/apply.html", {"form": form})


def thanks(request, reference):
    # Only the person who just applied can view their confirmation page
    if request.session.get("last_application") != reference:
        return redirect("admissions:index")
    app = get_object_or_404(Application, reference=reference)
    return render(request, "admissions/thanks.html", {"a": app})
