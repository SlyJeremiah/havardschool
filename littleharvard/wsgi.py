import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "littleharvard.settings")

application = get_wsgi_application()
# Vercel's Python runtime looks for a variable named `app`
app = application
