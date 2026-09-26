"""
Populate starter content so the site looks complete on first deploy.

Facts (name, tagline, address, phone, email, hours, Facebook) come from the school's
public Facebook page. Programme details, fees, steps and FAQs are sensible DEFAULTS
for a Zimbabwean ECD centre — review and edit them in the admin.

Usage:  python manage.py seed_site          (only fills empty tables)
        python manage.py seed_site --force  (also resets Site settings text)
"""
from datetime import date, time, timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from academics.models import Programme
from admissions.models import AdmissionStep, Requirement
from core.models import FAQ, Feature, SiteSettings
from news.models import Event, Post

ABOUT = """Little Harvard ECD Centre is an Early Childhood Development centre at 87 Link Drive, Southwood, in Kwekwe. We give children a joyful, safe and stimulating start to their education.

Our classrooms are full of hands-on activities that build fine motor skills, concentration, coordination, language and confidence. Children learn by doing: they sort, build, paint, sing, explore and play together.

Every year we celebrate our "little graduates" as they move on to primary school ready to shine. No doubt, the Little Graduate is hatched here!"""

FEATURES = [
    ("Hands-on learning", "Children learn by touching, building and exploring, which develops fine motor skills, concentration and coordination.", "bi-puzzle"),
    ("Caring, qualified teachers", "Warm, trained ECD practitioners who know every child by name and nurture their individual strengths.", "bi-heart"),
    ("School-ready graduates", "A structured, play-based ECD curriculum that prepares learners for a confident start in Grade 1.", "bi-mortarboard"),
    ("Language & vocabulary", "Stories, rhymes, songs and conversation grow early literacy and vocabulary in English and local languages.", "bi-book"),
    ("Creative arts & music", "Painting, craft, music and movement help children express themselves and build confidence.", "bi-palette"),
    ("Safe & secure environment", "A secure, child-friendly campus in Southwood with close supervision throughout the day.", "bi-shield-check"),
]

PROGRAMMES = [
    dict(name="Baby Class", slug="baby-class", age_range="2 – 3 years", color="green", order=1,
         summary="A gentle first step into school: routines, social play and early language in a nurturing setting.",
         description="Our Baby Class introduces toddlers to a school routine in a warm, homely environment.\n\n"
                     "Through sensory play, songs, stories and simple activities, children build independence, "
                     "confidence and early communication skills.",
         learning_areas="Sensory play\nEarly language & rhymes\nSocial & emotional skills\nGross motor play\nIndependence & self-care\nMusic & movement",
         daily_schedule="07:30 – Arrival & free play\n08:30 – Circle time & rhymes\n09:30 – Snack time\n10:00 – Sensory & outdoor play\n11:00 – Story time\n12:00 – Lunch & rest"),
    dict(name="ECD A", slug="ecd-a", age_range="3 – 4 years", color="primary", order=2,
         summary="Play-based learning that builds early numeracy, literacy, fine motor skills and curiosity.",
         description="ECD A follows the Zimbabwe ECD curriculum through structured play and hands-on activities.\n\n"
                     "Learners explore colours, shapes, numbers and letters, and develop the fine motor skills, "
                     "concentration and coordination needed for later learning.",
         learning_areas="Early numeracy\nPre-reading & phonics\nFine motor skills\nLanguage & vocabulary\nCreative arts\nPhysical education\nEnvironmental science\nSocial skills",
         daily_schedule="07:30 – Arrival & free play\n08:00 – Assembly & circle time\n08:30 – Numeracy activities\n09:30 – Snack & outdoor play\n10:15 – Language & phonics\n11:00 – Art, music or PE\n12:00 – Lunch\n12:30 – Story time & home time"),
    dict(name="ECD B", slug="ecd-b", age_range="4 – 5 years", color="orange", order=3,
         summary="Our graduating class — confident readers, counters and communicators ready for Grade 1.",
         description="ECD B consolidates early literacy and numeracy and prepares children for a smooth move to Grade 1.\n\n"
                     "Learners read simple words, write their names, count and solve simple problems, and take part "
                     "in projects, concerts and our much-loved graduation ceremony.",
         learning_areas="Reading & writing readiness\nNumeracy & problem solving\nFine motor & handwriting\nScience & discovery\nICT awareness\nPerforming arts\nPhysical education\nSchool readiness",
         daily_schedule="07:30 – Arrival\n08:00 – Assembly\n08:15 – Literacy\n09:15 – Numeracy\n10:00 – Snack & outdoor play\n10:30 – Science / discovery\n11:15 – Arts, music or PE\n12:00 – Lunch\n12:45 – Story time & home time"),
    dict(name="Day Care & After School", slug="day-care", age_range="2 – 6 years", color="navy", order=4,
         summary="Extended supervised care with rest, meals, homework support and play for working parents.",
         description="For families who need longer hours, our day care and after-school programme offers safe, "
                     "supervised care until the end of the working day.\n\n"
                     "Children rest, eat, play and enjoy quiet activities and reading with caring staff.",
         learning_areas="Supervised play\nRest time\nHomework & reading support\nCreative activities",
         hours="Until 16:00 (Mon – Thu), 13:00 (Fri)"),
]

STEPS = [
    ("Enquire or visit", "Call, WhatsApp or send us a message to book a tour of the centre and meet our teachers."),
    ("Apply online", "Fill in our short online application form. You'll get a reference number straight away."),
    ("Submit documents", "Bring your child's documents to the office (see the list below)."),
    ("Pay & start", "Pay the registration and term fees, collect the uniform and requirements list, and your child is ready to start!"),
]

REQUIREMENTS = [
    "Copy of the child's birth certificate",
    "Copy of the child's immunisation / clinic card",
    "Two recent passport-size photos of the child",
    "Copy of parent / guardian national ID",
    "Previous school report (if applicable)",
    "Completed application form",
]

FAQS = [
    ("What ages do you accept?", "We welcome children from about 2 years (Baby Class) up to 5–6 years (ECD B). Contact us if you're unsure which class suits your child."),
    ("What are your school hours?", "Monday to Thursday 08:00 – 16:00 and Friday 08:00 – 13:00. Early drop-off and day care may be available, so please ask the office."),
    ("Is the centre registered?", "Yes. Little Harvard is registered with the Ministry of Primary and Secondary Education and follows the national ECD curriculum."),
    ("Can I visit before enrolling?", "Absolutely. We encourage parents to visit, see the classrooms and meet the teachers. Book a visit by phone, WhatsApp or through the online application."),
    ("How do I pay fees?", "Please contact the office for the current fee structure and accepted payment methods."),
]


class Command(BaseCommand):
    help = "Seed starter content for the Little Harvard website."

    def add_arguments(self, parser):
        parser.add_argument("--force", action="store_true", help="Overwrite Site settings text fields.")

    def handle(self, *args, force=False, **opts):
        s = SiteSettings.load()
        if force or not s.about_intro:
            s.about_intro = ABOUT
            s.mission = ("To provide a safe, loving and stimulating environment where every child develops "
                         "socially, emotionally, physically and intellectually through play-based learning.")
            s.vision = "To be Kwekwe's leading early childhood centre, hatching confident, curious and school-ready little graduates."
            s.core_values = "Love & care\nCuriosity\nRespect\nExcellence\nSafety\nPartnership with parents"
            s.save()
            self.stdout.write("+ Site settings")

        self._fill(Feature, [dict(title=t, description=d, icon=i, order=n) for n, (t, d, i) in enumerate(FEATURES)])
        self._fill(Programme, PROGRAMMES)
        self._fill(AdmissionStep, [dict(title=t, description=d, order=n) for n, (t, d) in enumerate(STEPS)])
        self._fill(Requirement, [dict(text=t, order=n) for n, t in enumerate(REQUIREMENTS)])
        self._fill(FAQ, [dict(question=q, answer=a, order=n) for n, (q, a) in enumerate(FAQS)])

        self._fill(Post, [dict(
            title="Learning the parts of the face",
            category="activity",
            body="Our ECD learners explored the parts of the face through a fun, hands-on activity. "
                 "Along the way they developed their fine motor skills, concentration, coordination and vocabulary.\n\n"
                 "Activities like this help children name and understand their bodies while practising the careful hand "
                 "movements they will later use for writing.",
            published_at=timezone.now() - timedelta(days=2),
        ), dict(
            title="Welcome to our new website!",
            category="announcement",
            body="We're excited to launch the new Little Harvard ECD Centre website. Parents can now read school news, "
                 "view our gallery, check upcoming events and apply online.\n\n"
                 "Keep following us on Facebook for daily classroom videos and reels.",
        )])

        today = timezone.localdate()
        grad = date(today.year, 11, 28) if today < date(today.year, 11, 28) else date(today.year + 1, 11, 27)
        self._fill(Event, [dict(
            title="ECD B Graduation Ceremony", slug="ecd-b-graduation",
            date=grad, start_time=time(9, 0), end_time=time(13, 0),
            description="Join us as we celebrate our little graduates! Parents and guardians are warmly invited. "
                        "Please confirm the final date and details with the office.",
        )])
        self.stdout.write(self.style.SUCCESS("Seeding complete. Review content in /admin/."))

    def _fill(self, model, rows):
        if model.objects.exists():
            self.stdout.write(f"- {model._meta.verbose_name_plural} already has data — skipped")
            return
        for row in rows:
            model.objects.create(**row)
        self.stdout.write(f"+ {model._meta.verbose_name_plural} ({len(rows)})")
