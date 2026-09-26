from datetime import date
from io import StringIO

from django.core import mail
from django.core.management import call_command
from django.test import TestCase, override_settings
from django.urls import reverse

from academics.models import Programme
from admissions.models import Application
from core.models import ContactMessage
from gallery.models import Album
from news.models import Event, Post
from news.templatetags.embeds import video_embed_url


@override_settings(EMAIL_BACKEND="django.core.mail.backends.locmem.EmailBackend",
                   SCHOOL_NOTIFY_EMAILS=["office@example.test"],
                   STORAGES={"default": {"BACKEND": "django.core.files.storage.InMemoryStorage"},
                             "staticfiles": {"BACKEND": "django.contrib.staticfiles.storage.StaticFilesStorage"}})
class SiteTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        call_command("seed_site", stdout=StringIO())
        Album.objects.create(title="Graduation", slug="graduation")

    def test_public_pages_render(self):
        urls = [
            reverse("core:home"), reverse("core:about"), reverse("core:contact"),
            reverse("academics:list"), Programme.objects.first().get_absolute_url(),
            reverse("admissions:index"), reverse("admissions:apply"),
            reverse("news:list"), reverse("news:list") + "?category=activity",
            Post.objects.first().get_absolute_url(),
            reverse("news:events"), Event.objects.first().get_absolute_url(),
            reverse("gallery:list"), reverse("gallery:detail", args=["graduation"]),
            "/sitemap.xml", "/robots.txt",
        ]
        for url in urls:
            with self.subTest(url=url):
                self.assertEqual(self.client.get(url).status_code, 200)

    def test_404(self):
        self.assertEqual(self.client.get("/nope/").status_code, 404)

    def test_contact_form_saves_and_emails(self):
        r = self.client.post(reverse("core:contact"), {
            "name": "Rudo", "email": "rudo@example.test", "phone": "0770000000",
            "subject": "Fees", "message": "Hello", "website": "",
        })
        self.assertRedirects(r, reverse("core:contact"))
        self.assertEqual(ContactMessage.objects.count(), 1)
        self.assertEqual(len(mail.outbox), 2)
        self.assertEqual(mail.outbox[0].to, ["office@example.test"])
        self.assertEqual(mail.outbox[0].reply_to, ["rudo@example.test"])

    def test_honeypot_blocks_spam(self):
        self.client.post(reverse("core:contact"), {
            "name": "Bot", "email": "b@example.test", "subject": "x", "message": "x", "website": "spam.com"})
        self.assertEqual(ContactMessage.objects.count(), 0)

    def test_application_flow(self):
        p = Programme.objects.get(slug="ecd-a")
        r = self.client.post(reverse("admissions:apply"), {
            "child_first_name": "Tino", "child_last_name": "Moyo",
            "child_dob": date(date.today().year - 4, 3, 1).isoformat(), "child_gender": "boy",
            "programme": p.pk, "start_term": "term1", "start_year": date.today().year + 1,
            "parent_name": "Chipo Moyo", "relationship": "Mother", "parent_phone": "0771234567",
            "parent_email": "chipo@example.test", "wants_visit": "on", "consent": "on", "website": "",
        })
        app = Application.objects.get()
        self.assertRedirects(r, reverse("admissions:thanks", args=[app.reference]))
        self.assertTrue(app.reference.startswith("LH"))
        self.assertEqual(len(mail.outbox), 2)
        self.assertContains(self.client.get(r.url), app.reference)
        # Another visitor can't see the confirmation page
        self.client.session.flush()
        self.client.cookies.clear()
        self.assertEqual(self.client.get(r.url).status_code, 302)

    def test_application_rejects_old_child(self):
        r = self.client.post(reverse("admissions:apply"), {
            "child_first_name": "A", "child_last_name": "B", "child_dob": "2010-01-01",
            "child_gender": "girl", "start_term": "term1", "start_year": date.today().year,
            "parent_name": "P", "relationship": "Parent", "parent_phone": "1",
            "parent_email": "p@example.test", "consent": "on"})
        self.assertEqual(r.status_code, 200)
        self.assertEqual(Application.objects.count(), 0)

    def test_video_embeds(self):
        self.assertIn("youtube-nocookie.com/embed/dQw4w9WgXcQ",
                      video_embed_url("https://youtu.be/dQw4w9WgXcQ"))
        self.assertIn("facebook.com/plugins/video.php",
                      video_embed_url("https://www.facebook.com/reel/123"))
        self.assertEqual(video_embed_url("https://example.com"), "")
