from django.core.cache import cache
from django.db import models


class SiteSettings(models.Model):
    """Single row holding school-wide info editable from the admin."""

    school_name = models.CharField(max_length=120, default="Little Harvard ECD Centre")
    short_name = models.CharField(max_length=60, default="Little Harvard")
    tagline = models.CharField(max_length=200, default="No doubt, the Little Graduate is hatched here!")
    logo = models.ImageField(upload_to="site/", blank=True, help_text="Square PNG recommended.")
    hero_title = models.CharField(max_length=160, default="Where little minds hatch big dreams")
    hero_subtitle = models.TextField(
        default="A caring Early Childhood Development centre in Southwood, Kwekwe, where children "
        "learn through play, discovery and hands-on activities."
    )
    hero_image = models.ImageField(upload_to="site/", blank=True)

    about_intro = models.TextField(blank=True)
    mission = models.TextField(blank=True)
    vision = models.TextField(blank=True)
    core_values = models.TextField(blank=True, help_text="One value per line.")
    about_image = models.ImageField(upload_to="site/", blank=True)

    address = models.CharField(max_length=200, default="87 Link Drive, Southwood, Kwekwe, Zimbabwe")
    phone = models.CharField(max_length=40, default="079 020 5518")
    phone_alt = models.CharField(max_length=40, blank=True, default="055 252 3573")
    whatsapp = models.CharField(
        max_length=20, blank=True, default="263790205518", help_text="International format, digits only."
    )
    email = models.EmailField(default="lilharvard5@gmail.com")
    office_hours = models.TextField(
        default="Monday – Thursday: 08:00 – 16:00\nFriday: 08:00 – 13:00\nSaturday – Sunday: Closed",
        help_text="One line per row.",
    )
    map_query = models.CharField(
        max_length=200, default="87 Link Drive, Southwood, Kwekwe, Zimbabwe",
        help_text="Address or coordinates used for the Google Map embed.",
    )

    facebook_url = models.URLField(blank=True, default="https://www.facebook.com/lilharvard5")
    instagram_url = models.URLField(blank=True)
    tiktok_url = models.URLField(blank=True)
    youtube_url = models.URLField(blank=True)

    stat_learners = models.PositiveIntegerField(default=0, help_text="Shown on homepage if > 0")
    stat_teachers = models.PositiveIntegerField(default=0)
    stat_years = models.PositiveIntegerField(default=0)
    stat_graduates = models.PositiveIntegerField(default=0)

    admissions_open = models.BooleanField(default=True)
    admissions_banner = models.CharField(
        max_length=200, blank=True, default="Enrolment is now open for the new term — book a visit today!"
    )
    meta_description = models.CharField(
        max_length=300,
        default="Little Harvard ECD Centre in Southwood, Kwekwe, Zimbabwe — quality early childhood "
        "education (ECD A & B), play-based learning and a caring environment.",
    )

    class Meta:
        verbose_name = "Site settings"
        verbose_name_plural = "Site settings"

    def __str__(self):
        return "Site settings"

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)
        cache.delete("site_settings")

    @classmethod
    def load(cls):
        obj = cache.get("site_settings")
        if obj is None:
            obj, _ = cls.objects.get_or_create(pk=1)
            cache.set("site_settings", obj, 300)
        return obj

    @property
    def office_hours_lines(self):
        return [l for l in self.office_hours.splitlines() if l.strip()]

    @property
    def core_values_list(self):
        return [l.strip() for l in self.core_values.splitlines() if l.strip()]

    @property
    def phone_link(self):
        digits = "".join(c for c in self.phone if c.isdigit())
        if digits.startswith("0"):
            digits = "263" + digits[1:]
        return f"+{digits}"


class Feature(models.Model):
    """'Why choose us' highlights on the homepage."""

    ICONS = [
        ("bi-puzzle", "Puzzle"), ("bi-palette", "Palette"), ("bi-heart", "Heart"),
        ("bi-shield-check", "Shield"), ("bi-book", "Book"), ("bi-music-note-beamed", "Music"),
        ("bi-tree", "Tree"), ("bi-mortarboard", "Graduation cap"), ("bi-people", "People"),
        ("bi-egg-fried", "Meals"), ("bi-bus-front", "Transport"), ("bi-brush", "Art"),
        ("bi-emoji-smile", "Smile"), ("bi-star", "Star"), ("bi-translate", "Language"),
    ]
    title = models.CharField(max_length=80)
    description = models.TextField()
    icon = models.CharField(max_length=40, choices=ICONS, default="bi-star")
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title


class StaffMember(models.Model):
    name = models.CharField(max_length=100)
    role = models.CharField(max_length=100)
    bio = models.TextField(blank=True)
    photo = models.ImageField(upload_to="staff/", blank=True)
    order = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ["order", "name"]
        verbose_name = "staff member"

    def __str__(self):
        return f"{self.name} — {self.role}"


class Testimonial(models.Model):
    author = models.CharField(max_length=100)
    relation = models.CharField(max_length=100, blank=True, help_text='e.g. "Parent of an ECD B learner"')
    quote = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5)
    is_published = models.BooleanField(default=True)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "-id"]

    def __str__(self):
        return self.author


class FAQ(models.Model):
    question = models.CharField(max_length=200)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]
        verbose_name = "FAQ"
        verbose_name_plural = "FAQs"

    def __str__(self):
        return self.question


class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=40, blank=True)
    subject = models.CharField(max_length=150)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_handled = models.BooleanField(default=False)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.name}: {self.subject}"
