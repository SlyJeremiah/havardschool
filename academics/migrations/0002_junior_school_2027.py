"""Apply the 2027 Harvard Junior School (Grades 1 – 4) update to an already-seeded site.

Fresh installs get this content from `seed_site`, so this does nothing on an empty database.
Site settings are only changed where they still hold the original default text, so edits
made in the admin are never overwritten.
"""
import logging

from django.conf import settings
from django.db import migrations

from academics.junior_content import (
    AGES_FAQ_ANSWER, AGES_FAQ_QUESTION, ANNOUNCEMENT, JUNIOR_FAQ, JUNIOR_PROGRAMME, JUNIOR_REQUIREMENT,
)

logger = logging.getLogger(__name__)

OLD_ADDRESS = "87 Link Drive, Southwood, Kwekwe, Zimbabwe"
NEW_ADDRESS = "87 Link Drive, Southwood, Masasa Park, Kwekwe, Zimbabwe"
OLD_BANNER = "Enrolment is now open for the new term — book a visit today!"
NEW_BANNER = "Enrolment in progress for the 2027 academic year — now offering Grades 1 – 4!"
OLD_HERO = ("A caring Early Childhood Development centre in Southwood, Kwekwe, where children "
            "learn through play, discovery and hands-on activities.")
NEW_HERO = ("A caring Early Childhood Development centre and junior school (Grades 1 – 4) in Southwood, "
            "Kwekwe, where children learn through play, discovery and hands-on activities.")
OLD_META = ("Little Harvard ECD Centre in Southwood, Kwekwe, Zimbabwe — quality early childhood "
            "education (ECD A & B), play-based learning and a caring environment.")
NEW_META = ("Little Harvard ECD Centre in Southwood, Kwekwe, Zimbabwe — quality early childhood "
            "education (ECD A & B) and Harvard Junior School (Grades 1 – 4) in a caring environment.")
OLD_AGES_ANSWER = ("We welcome children from about 2 years (Baby Class) up to 5–6 years (ECD B). "
                   "Contact us if you're unsure which class suits your child.")


def forwards(apps, schema_editor):
    Programme = apps.get_model("academics", "Programme")
    SiteSettings = apps.get_model("core", "SiteSettings")
    FAQ = apps.get_model("core", "FAQ")
    Requirement = apps.get_model("admissions", "Requirement")
    Post = apps.get_model("news", "Post")

    if not Programme.objects.exists():
        return  # fresh install: seed_site provides everything

    s = SiteSettings.objects.filter(pk=1).first()
    if s:
        for field, old, new in [("address", OLD_ADDRESS, NEW_ADDRESS), ("map_query", OLD_ADDRESS, NEW_ADDRESS),
                                ("admissions_banner", OLD_BANNER, NEW_BANNER), ("hero_subtitle", OLD_HERO, NEW_HERO),
                                ("meta_description", OLD_META, NEW_META)]:
            if getattr(s, field) == old:
                setattr(s, field, new)
        s.admissions_open = True
        s.save()

    Programme.objects.get_or_create(slug=JUNIOR_PROGRAMME["slug"], defaults=JUNIOR_PROGRAMME)

    if not Requirement.objects.filter(text=JUNIOR_REQUIREMENT).exists():
        Requirement.objects.create(text=JUNIOR_REQUIREMENT, order=Requirement.objects.count())

    FAQ.objects.filter(question=AGES_FAQ_QUESTION, answer=OLD_AGES_ANSWER).update(answer=AGES_FAQ_ANSWER)
    if not FAQ.objects.filter(question=JUNIOR_FAQ[0]).exists():
        FAQ.objects.create(question=JUNIOR_FAQ[0], answer=JUNIOR_FAQ[1], order=1)

    if not Post.objects.filter(slug=ANNOUNCEMENT["slug"]).exists():
        post = Post(**ANNOUNCEMENT)
        # Attach the flyer as the cover (goes to Backblaze B2 in production); skip if storage fails
        try:
            from django.core.files import File

            with open(settings.BASE_DIR / "static" / "img" / "junior-2027-flyer.jpg", "rb") as fh:
                post.cover_image.save("junior-2027-flyer.jpg", File(fh), save=False)
        except Exception:
            logger.warning("Could not upload the 2027 flyer as the post cover; saving without it.", exc_info=True)
            post.cover_image = ""
        post.save()


class Migration(migrations.Migration):

    dependencies = [
        ("academics", "0001_initial"),
        ("core", "0002_alter_sitesettings_address_and_more"),
        ("admissions", "0002_application_grade"),
        ("news", "0001_initial"),
    ]

    operations = [migrations.RunPython(forwards, migrations.RunPython.noop)]
