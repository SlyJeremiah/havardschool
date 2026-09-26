from django.db import models
from django.urls import reverse


class Programme(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    age_range = models.CharField(max_length=60, help_text='e.g. "3 – 4 years"')
    summary = models.CharField(max_length=250)
    description = models.TextField(help_text="Blank lines separate paragraphs.")
    learning_areas = models.TextField(blank=True, help_text="One learning area per line.")
    daily_schedule = models.TextField(blank=True, help_text='One per line, e.g. "07:30 – Arrival & free play"')
    class_size = models.CharField(max_length=60, blank=True)
    hours = models.CharField(max_length=100, blank=True)
    fees = models.CharField(max_length=150, blank=True, help_text="Leave blank to show 'Contact us'.")
    image = models.ImageField(upload_to="programmes/", blank=True)
    color = models.CharField(
        max_length=20, default="primary",
        choices=[("primary", "Yellow"), ("orange", "Orange"), ("green", "Green"), ("navy", "Navy")],
    )
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "name"]

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("academics:detail", args=[self.slug])

    @property
    def learning_areas_list(self):
        return [l.strip() for l in self.learning_areas.splitlines() if l.strip()]

    @property
    def schedule_list(self):
        rows = []
        for line in self.daily_schedule.splitlines():
            if not line.strip():
                continue
            time, _, activity = line.partition("–") if "–" in line else line.partition("-")
            rows.append((time.strip(), activity.strip()))
        return rows
