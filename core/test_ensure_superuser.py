import os
from io import StringIO
from unittest import mock

from django.contrib.auth.models import User
from django.core.management import call_command
from django.test import TestCase

ENV = {"DJANGO_SUPERUSER_USERNAME": "head", "DJANGO_SUPERUSER_EMAIL": "head@example.test",
       "DJANGO_SUPERUSER_PASSWORD": "Kwekwe-Graduates-2027!"}


def run(env):
    out, err = StringIO(), StringIO()
    with mock.patch.dict(os.environ, env, clear=False):
        for k in ENV:
            if k not in env:
                os.environ.pop(k, None)
        call_command("ensure_superuser", stdout=out, stderr=err)
    return out.getvalue() + err.getvalue()


class EnsureSuperuserTests(TestCase):
    def test_skips_without_variables(self):
        self.assertIn("skipping", run({}))
        self.assertFalse(User.objects.exists())

    def test_creates_superuser(self):
        output = run(ENV)
        u = User.objects.get(username="head")
        self.assertTrue(u.is_superuser and u.is_staff)
        self.assertTrue(u.check_password(ENV["DJANGO_SUPERUSER_PASSWORD"]))
        self.assertNotIn(ENV["DJANGO_SUPERUSER_PASSWORD"], output)

    def test_existing_user_untouched(self):
        User.objects.create_user("head", password="original-pass-123")
        self.assertIn("already exists", run(ENV))
        self.assertTrue(User.objects.get(username="head").check_password("original-pass-123"))

    def test_weak_password_rejected(self):
        output = run({**ENV, "DJANGO_SUPERUSER_PASSWORD": "1234"})
        self.assertIn("NOT created", output)
        self.assertFalse(User.objects.exists())
