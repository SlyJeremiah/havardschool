from django.shortcuts import get_object_or_404, render

from .models import Album, Video


def album_list(request):
    return render(request, "gallery/list.html", {
        "albums": Album.objects.filter(is_published=True).prefetch_related("photos"),
        "videos": Video.objects.filter(is_published=True)[:6],
    })


def album_detail(request, slug):
    album = get_object_or_404(Album, slug=slug, is_published=True)
    return render(request, "gallery/detail.html", {"album": album, "photos": album.photos.all()})
