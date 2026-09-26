from django.db import models
from django.urls import reverse
from django.utils import timezone

from core.images import optimise_image


class Album(models.Model):
    title = models.CharField(max_length=150)
    slug = models.SlugField(max_length=170, unique=True)
    description = models.TextField(blank=True)
    cover = models.ImageField(upload_to="gallery/covers/", blank=True,
                              help_text="Optional. The first photo is used if empty.")
    date = models.DateField(default=timezone.localdate)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["-date", "-id"]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("gallery:detail", args=[self.slug])

    @property
    def cover_image(self):
        if self.cover:
            return self.cover
        first = self.photos.first()
        return first.image if first else None


class Photo(models.Model):
    album = models.ForeignKey(Album, on_delete=models.CASCADE, related_name="photos")
    image = models.ImageField(upload_to="gallery/%Y/%m/")
    caption = models.CharField(max_length=200, blank=True)
    order = models.PositiveIntegerField(default=0)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["order", "-uploaded_at"]

    def __str__(self):
        return self.caption or f"Photo {self.pk}"

    def save(self, *args, **kwargs):
        optimise_image(self.image)
        super().save(*args, **kwargs)


class Video(models.Model):
    title = models.CharField(max_length=150)
    url = models.URLField(help_text="YouTube or Facebook video / reel link.")
    description = models.CharField(max_length=250, blank=True)
    date = models.DateField(default=timezone.localdate)
    is_published = models.BooleanField(default=True)

    class Meta:
        ordering = ["-date", "-id"]

    def __str__(self):
        return self.title
