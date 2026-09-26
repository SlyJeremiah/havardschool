from django.db import models
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify

from core.images import optimise_image


class PostQuerySet(models.QuerySet):
    def published(self):
        return self.filter(is_published=True, published_at__lte=timezone.now())


class Post(models.Model):
    CATEGORIES = [
        ("news", "News"),
        ("activity", "Classroom activity"),
        ("announcement", "Announcement"),
        ("celebration", "Celebration"),
        ("graduation", "Graduation"),
    ]
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    category = models.CharField(max_length=20, choices=CATEGORIES, default="news")
    excerpt = models.CharField(max_length=300, blank=True, help_text="Short summary for listings.")
    body = models.TextField(help_text="Blank lines separate paragraphs.")
    cover_image = models.ImageField(upload_to="news/", blank=True)
    video_url = models.URLField(
        blank=True, help_text="Optional YouTube or Facebook video/reel link to embed.")
    published_at = models.DateTimeField(default=timezone.now)
    is_published = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

    objects = PostQuerySet.as_manager()

    class Meta:
        ordering = ["-published_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            base = slugify(self.title)[:200] or "post"
            slug, n = base, 2
            while Post.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                slug, n = f"{base}-{n}", n + 1
            self.slug = slug
        if not self.excerpt:
            self.excerpt = self.body[:280]
        optimise_image(self.cover_image)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("news:detail", args=[self.slug])


class Event(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True)
    date = models.DateField()
    end_date = models.DateField(blank=True, null=True)
    start_time = models.TimeField(blank=True, null=True)
    end_time = models.TimeField(blank=True, null=True)
    location = models.CharField(max_length=200, default="Little Harvard ECD Centre, Southwood")
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to="events/", blank=True)

    class Meta:
        ordering = ["date", "start_time"]

    def __str__(self):
        return f"{self.title} ({self.date})"

    def get_absolute_url(self):
        return reverse("news:event_detail", args=[self.slug])

    @property
    def is_past(self):
        return (self.end_date or self.date) < timezone.localdate()
