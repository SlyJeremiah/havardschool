from datetime import date

from django import forms
from django.utils import timezone

from academics.models import Programme
from core.forms import BootstrapFormMixin, HoneypotMixin

from .models import Application


class ApplicationForm(BootstrapFormMixin, HoneypotMixin, forms.ModelForm):
    consent = forms.BooleanField(
        label="I confirm the information above is correct and agree to be contacted by the school.",
    )

    class Meta:
        model = Application
        fields = [
            "child_first_name", "child_last_name", "child_dob", "child_gender", "programme",
            "start_term", "start_year", "previous_school", "medical_notes",
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
        year = timezone.localdate().year
        self.fields["start_year"] = forms.TypedChoiceField(
            label="Year", coerce=int, choices=[(y, y) for y in (year, year + 1)],
            widget=forms.Select(attrs={"class": "form-select"}),
        )

    def clean_child_dob(self):
        dob = self.cleaned_data["child_dob"]
        today = date.today()
        age = (today - dob).days / 365.25
        if dob > today:
            raise forms.ValidationError("Date of birth cannot be in the future.")
        if age > 8:
            raise forms.ValidationError("Our centre caters for children up to 7 years old.")
        return dob
