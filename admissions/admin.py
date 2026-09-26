import csv

from django.contrib import admin
from django.http import HttpResponse

from .models import AdmissionStep, Application, Requirement


@admin.register(AdmissionStep)
class AdmissionStepAdmin(admin.ModelAdmin):
    list_display = ("title", "order")
    list_editable = ("order",)


@admin.register(Requirement)
class RequirementAdmin(admin.ModelAdmin):
    list_display = ("text", "order")
    list_editable = ("order",)


@admin.action(description="Export selected to CSV")
def export_csv(modeladmin, request, queryset):
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = 'attachment; filename="applications.csv"'
    fields = [f.name for f in Application._meta.fields]
    writer = csv.writer(response)
    writer.writerow(fields)
    for obj in queryset:
        writer.writerow([getattr(obj, f) for f in fields])
    return response


@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("reference", "child_name", "programme", "start_term", "start_year",
                    "parent_name", "parent_phone", "status", "created_at")
    list_filter = ("status", "programme", "start_term", "start_year", "wants_visit")
    list_editable = ("status",)
    search_fields = ("reference", "child_first_name", "child_last_name", "parent_name",
                     "parent_phone", "parent_email")
    readonly_fields = ("reference", "created_at")
    date_hierarchy = "created_at"
    actions = [export_csv]
    fieldsets = (
        ("Status", {"fields": ("reference", "status", "staff_notes", "created_at")}),
        ("Child", {"fields": ("child_first_name", "child_last_name", "child_dob", "child_gender",
                              "programme", "start_term", "start_year", "previous_school",
                              "medical_notes")}),
        ("Parent / guardian", {"fields": ("parent_name", "relationship", "parent_phone", "parent_email",
                                          "home_address", "how_heard", "wants_visit", "notes")}),
    )
