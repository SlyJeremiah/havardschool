from django.contrib import admin
from django.shortcuts import redirect
from django.urls import reverse

from .models import FAQ, ContactMessage, Feature, SiteSettings, StaffMember, Testimonial


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    fieldsets = (
        ("Identity", {"fields": ("school_name", "short_name", "tagline", "logo", "meta_description")}),
        ("Homepage hero", {"fields": ("hero_title", "hero_subtitle", "hero_image",
                                      "admissions_open", "admissions_banner")}),
        ("About", {"fields": ("about_intro", "mission", "vision", "core_values", "about_image")}),
        ("Contact", {"fields": ("address", "phone", "phone_alt", "whatsapp", "email",
                                "office_hours", "map_query")}),
        ("Social media", {"fields": ("facebook_url", "instagram_url", "tiktok_url", "youtube_url")}),
        ("Homepage stats", {"fields": ("stat_learners", "stat_teachers", "stat_years", "stat_graduates")}),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def changelist_view(self, request, extra_context=None):
        obj = SiteSettings.load()
        return redirect(reverse("admin:core_sitesettings_change", args=[obj.pk]))


@admin.register(Feature)
class FeatureAdmin(admin.ModelAdmin):
    list_display = ("title", "icon", "order")
    list_editable = ("order",)


@admin.register(StaffMember)
class StaffMemberAdmin(admin.ModelAdmin):
    list_display = ("name", "role", "order", "is_active")
    list_editable = ("order", "is_active")
    search_fields = ("name", "role")


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ("author", "relation", "rating", "is_published", "order")
    list_editable = ("is_published", "order")


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ("question", "order")
    list_editable = ("order",)


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ("name", "subject", "email", "phone", "created_at", "is_handled")
    list_filter = ("is_handled", "created_at")
    list_editable = ("is_handled",)
    search_fields = ("name", "email", "subject", "message")
    readonly_fields = ("name", "email", "phone", "subject", "message", "created_at")
