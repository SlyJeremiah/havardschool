"""
Create the first admin account from environment variables (used during the Vercel build).

    DJANGO_SUPERUSER_USERNAME
    DJANGO_SUPERUSER_EMAIL
    DJANGO_SUPERUSER_PASSWORD

Does nothing if any variable is missing or the username already exists, so it is safe to run
on every deploy. It never changes an existing account's password. Remove the variables from
Vercel once you have logged in.
"""
import os

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Create a superuser from DJANGO_SUPERUSER_* environment variables if it doesn't exist."

    def handle(self, *args, **options):
        username = os.environ.get("DJANGO_SUPERUSER_USERNAME", "").strip()
        email = os.environ.get("DJANGO_SUPERUSER_EMAIL", "").strip()
        password = os.environ.get("DJANGO_SUPERUSER_PASSWORD", "")

        if not (username and email and password):
            self.stdout.write("ensure_superuser: DJANGO_SUPERUSER_* variables not set - skipping.")
            return

        User = get_user_model()
        if User.objects.filter(username=username).exists():
            self.stdout.write(f"ensure_superuser: '{username}' already exists - nothing to do. "
                              "You can now remove the DJANGO_SUPERUSER_* variables from Vercel.")
            return

        user = User(username=username, email=email, is_staff=True, is_superuser=True)
        try:
            validate_password(password, user)
        except ValidationError as exc:
            # Don't fail the deploy; explain why (without ever printing the password)
            self.stderr.write(self.style.WARNING(
                "ensure_superuser: password rejected, account NOT created: " + " ".join(exc.messages)))
            return

        user.set_password(password)
        user.save()
        self.stdout.write(self.style.SUCCESS(f"ensure_superuser: created admin account '{username}'."))
