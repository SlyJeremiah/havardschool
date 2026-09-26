from django.db import models
from django.utils import timezone


class AdmissionStep(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.title


class Requirement(models.Model):
    text = models.CharField(max_length=200)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ["order", "id"]

    def __str__(self):
        return self.text


class Application(models.Model):
    STATUS = [
        ("new", "New"),
        ("contacted", "Contacted"),
        ("visit", "Visit booked"),
        ("accepted", "Accepted"),
        ("waitlist", "Waiting list"),
        ("declined", "Declined"),
    ]
    TERMS = [("term1", "Term 1 (January)"), ("term2", "Term 2 (May)"), ("term3", "Term 3 (September)")]
    GENDER = [("girl", "Girl"), ("boy", "Boy")]

    reference = models.CharField(max_length=20, unique=True, editable=False)
    child_first_name = models.CharField("Child's first name", max_length=60)
    child_last_name = models.CharField("Child's surname", max_length=60)
    child_dob = models.DateField("Child's date of birth")
    child_gender = models.CharField("Gender", max_length=10, choices=GENDER)
    programme = models.ForeignKey(
        "academics.Programme", on_delete=models.SET_NULL, null=True, blank=True,
        verbose_name="Programme applying for",
    )
    start_term = models.CharField("Preferred start term", max_length=10, choices=TERMS)
    start_year = models.PositiveIntegerField("Year")
    previous_school = models.CharField(max_length=120, blank=True)
    medical_notes = models.TextField("Allergies / medical or special needs", blank=True)

    parent_name = models.CharField("Parent / guardian full name", max_length=120)
    relationship = models.CharField(max_length=40, default="Parent")
    parent_phone = models.CharField("Phone / WhatsApp", max_length=40)
    parent_email = models.EmailField("Email address")
    home_address = models.CharField(max_length=200, blank=True)
    how_heard = models.CharField("How did you hear about us?", max_length=100, blank=True)
    wants_visit = models.BooleanField("I would like to book a school visit", default=True)
    notes = models.TextField("Anything else we should know?", blank=True)

    status = models.CharField(max_length=20, choices=STATUS, default="new")
    staff_notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.reference} — {self.child_first_name} {self.child_last_name}"

    def save(self, *args, **kwargs):
        if not self.reference:
            year = timezone.localdate().year
            count = Application.objects.filter(created_at__year=year).count() + 1
            ref = f"LH{year}-{count:04d}"
            while Application.objects.filter(reference=ref).exists():
                count += 1
                ref = f"LH{year}-{count:04d}"
            self.reference = ref
        super().save(*args, **kwargs)

    @property
    def child_name(self):
        return f"{self.child_first_name} {self.child_last_name}"
