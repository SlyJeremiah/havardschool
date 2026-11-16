from django.conf import settings

from .models import SiteSettings


def site(request):
    return {
        "site": SiteSettings.load(),
        "GA_MEASUREMENT_ID": settings.GA_MEASUREMENT_ID,
        "SITE_URL": settings.SITE_URL,
        "ASSET_VERSION": settings.ASSET_VERSION,
    }
