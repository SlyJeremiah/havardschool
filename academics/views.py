from django.shortcuts import get_object_or_404, render

from .models import Programme


def programme_list(request):
    return render(request, "academics/list.html", {
        "programmes": Programme.objects.filter(is_active=True),
    })


def programme_detail(request, slug):
    programme = get_object_or_404(Programme, slug=slug, is_active=True)
    others = Programme.objects.filter(is_active=True).exclude(pk=programme.pk)
    return render(request, "academics/detail.html", {"programme": programme, "others": others})
