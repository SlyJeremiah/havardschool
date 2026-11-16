"""Harvard Junior School (Grades 1 – 4) content, from the 2027 enrolment flyer.

Shared by the seed command (fresh installs) and data migration 0002 (existing sites).
"""

JUNIOR_SLUG = "junior-school"

JUNIOR_PROGRAMME = dict(
    name="Harvard Junior School",
    slug=JUNIOR_SLUG,
    age_range="Grades 1 – 4",
    color="orange",
    order=10,
    summary="Where Dreams Take Flight: our junior primary school, now enrolling Grades 1 – 4 "
            "for the 2027 academic year.",
    description="Harvard Junior School is the next step for our little graduates. It continues the "
                "warm, hands-on approach of Little Harvard ECD Centre into the primary years, at the "
                "same campus on Link Drive.\n\n"
                "Learners in Grades 1 – 4 build strong foundations in literacy, numeracy and "
                "problem-solving in bright, well-resourced classrooms. Small classes and caring "
                "teachers help every child grow in confidence.\n\n"
                "Enrolment for the 2027 academic year is now in progress. The stationery and "
                "uniform list is provided upon registration.",
    learning_areas="English & literacy\nMathematics\nIndigenous languages\nScience & technology\n"
                   "Social studies (Heritage)\nVisual & performing arts\nPhysical education & sport\n"
                   "Family, religion & moral education\nICT",
    class_size="Small classes",
    hours="Mon – Thu 08:00 – 16:00, Fri 08:00 – 13:00",
)

JUNIOR_REQUIREMENT = "Stationery & uniform list (provided upon registration)"

JUNIOR_FAQ = (
    "Do you offer primary school grades?",
    "Yes! Harvard Junior School, on the same campus, now offers Grades 1 – 4. Enrolment for the "
    "2027 academic year is in progress. Apply online and choose “Harvard Junior School”, or call "
    "0790 205 518.",
)

AGES_FAQ_QUESTION = "What ages do you accept?"
AGES_FAQ_ANSWER = ("We welcome children from about 2 years (Baby Class) through ECD A and ECD B, and "
                   "up to Grade 4 at Harvard Junior School. Contact us if you're unsure which class "
                   "suits your child.")

ANNOUNCEMENT = dict(
    title="Enrolment in progress for 2027: now offering Grades 1 – 4",
    slug="enrolment-2027-grades-1-4",
    category="announcement",
    is_featured=True,
    excerpt="Harvard Junior School is now enrolling Grades 1 – 4 for the 2027 academic year.",
    body="We are excited to announce that Harvard Junior School is now offering Grades 1 – 4. "
         "Enrolment for the 2027 academic year is in progress!\n\n"
         "Our junior school continues the caring, hands-on learning our ECD learners love, in bright "
         "and colourful classrooms on our Link Drive campus.\n\n"
         "The stationery and uniform list is provided upon registration.\n\n"
         "Call 0790 205 518, visit us at 87 Link Drive, Southwood, Masasa Park, Kwekwe, or apply "
         "online today.",
)
