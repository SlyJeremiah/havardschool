from datetime import date

from django import forms
from django.utils import timezone

from academics.models import Programme
from core.forms import BootstrapFormMixin, HoneypotMixin

from .models import Application

JUNIOR_SLUG = "junior-school"


class ApplicationForm(BootstrapFormMixin, HoneypotMixin, forms.ModelForm):
    consent = forms.BooleanField(
        label="I confirm the information above is correct and agree to be contacted by the school.",
    )

    class Meta:
        model = Application
        fields = [
            "child_first_name", "child_last_name", "child_dob", "child_gender", "programme",
            "grade", "start_term", "start_year", "previous_school", "medical_notes",
            "parent_name", "relationship", "parent_phone", "parent_email", "home_address",
            "how_heard", "wants_visit", "notes",
        ]
        widgets = {
            "child_dob": forms.DateInput(attrs={"type": "date"}),
            "medical_notes": forms.Textarea(attrs={"rows": 2}),
            "notes": forms.Textarea(attrs={"rows": 3}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["programme"].queryset = Programme.objects.filter(is_active=True)
        self.fields["programme"].empty_label = "Not sure — please advise"
        self.fields["grade"].choices = [("", "Not applicable (ECD)")] + Application.GRADES
        today = timezone.localdate()
        year = today.year
        self.fields["start_year"] = forms.TypedChoiceField(
            label="Year", coerce=int, choices=[(y, y) for y in (year, year + 1)],
            # From September we're enrolling for the next academic year
            initial=year + 1 if today.month >= 9 else year,
            widget=forms.Select(attrs={"class": "form-select"}),
        )

    def clean_child_dob(self):
        dob = self.cleaned_data["child_dob"]
        today = date.today()
        age = (today - dob).days / 365.25
        if dob > today:
            raise forms.ValidationError("Date of birth cannot be in the future.")
        if age > 11:
            raise forms.ValidationError(
                "We cater for children from ECD up to Grade 4 (about 10 years old).")
        return dob

    def clean(self):
        data = super().clean()
        programme, grade = data.get("programme"), data.get("grade")
        junior = programme is not None and programme.slug == JUNIOR_SLUG
        if junior and not grade:
            self.add_error("grade", "Please choose the grade you are applying for.")
        if grade and programme is None:
            data["programme"] = Programme.objects.filter(slug=JUNIOR_SLUG).first()
        elif grade and not junior:
            self.add_error("grade", "Grades 1 – 4 are part of Harvard Junior School — "
                                    "choose “Harvard Junior School” as the programme.")
        return data
