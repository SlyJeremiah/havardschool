from django.apps import AppConfig
from django.contrib.admin import apps as admin_apps


class CoreConfig(AppConfig):
    default = True
    default_auto_field = "django.db.models.BigAutoField"
    name = "core"
    verbose_name = "Website & School Info"


class LittleHarvardAdminConfig(admin_apps.AdminConfig):
    """Replaces django.contrib.admin so every model registers on the branded dashboard site."""

    default = False  # only used when named explicitly in INSTALLED_APPS
    default_site = "core.admin_site.LittleHarvardAdminSite"
