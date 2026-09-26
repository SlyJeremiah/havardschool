from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, render
from django.utils import timezone

from .models import Event, Post


def post_list(request):
    posts = Post.objects.published()
    category = request.GET.get("category")
    if category in dict(Post.CATEGORIES):
        posts = posts.filter(category=category)
    page = Paginator(posts, 9).get_page(request.GET.get("page"))
    return render(request, "news/list.html", {
        "page": page,
        "categories": Post.CATEGORIES,
        "active_category": category,
        "upcoming": Event.objects.filter(date__gte=timezone.localdate())[:4],
    })


def post_detail(request, slug):
    post = get_object_or_404(Post.objects.published(), slug=slug)
    related = Post.objects.published().exclude(pk=post.pk).filter(category=post.category)[:3]
    return render(request, "news/detail.html", {"post": post, "related": related})


def event_list(request):
    today = timezone.localdate()
    return render(request, "news/events.html", {
        "upcoming": Event.objects.filter(date__gte=today),
        "past": Event.objects.filter(date__lt=today).order_by("-date")[:12],
    })


def event_detail(request, slug):
    event = get_object_or_404(Event, slug=slug)
    return render(request, "news/event_detail.html", {"event": event})
