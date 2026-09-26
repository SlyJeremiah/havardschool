# Little Harvard ECD Centre — Website

Django website for **Little Harvard ECD Centre**, 87 Link Drive, Southwood, Kwekwe, Zimbabwe
("No doubt, the Little Graduate is hatched here!").

| Layer        | Choice                                   |
|--------------|------------------------------------------|
| Backend      | Python 3.12 + Django 5.2 LTS             |
| Database     | PostgreSQL (Neon / Supabase free tier)   |
| Hosting      | Vercel (serverless Python + static CDN)  |
| Media        | Backblaze B2 via `django-storages` (S3)  |
| UI           | Bootstrap 5.3 + Bootstrap Icons (CDN)    |
| Email        | Gmail SMTP with an App Password          |
| Analytics    | Google Analytics 4 (+ CTA/form events)   |

## Features

- **Home**: hero, stats, "why choose us", programmes, latest news, upcoming events, gallery strip, testimonials
- **About**: story, mission/vision/values, approach, staff profiles
- **Programmes**: Baby Class, ECD A, ECD B, Day Care (all editable), each with learning areas, daily timetable and fees
- **Admissions**: steps, requirements, fee table, FAQ, and an **online application form** that saves to the DB, emails the school, sends the parent a confirmation with a reference number (`LH2026-0001`), and can be exported to CSV from the admin
- **News & Events**: categories, pagination, YouTube/Facebook reel embeds, WhatsApp/Facebook share, events calendar
- **Gallery**: albums with a lightbox, bulk photo upload in the admin, automatic image resizing (saves B2 storage), video section
- **Contact**: form (with spam honeypot) that emails the office, Google Map, WhatsApp button
- SEO: meta/OpenGraph tags, schema.org `Preschool` JSON-LD, `sitemap.xml`, `robots.txt`
- Everything (phone, hours, hero text, banner, social links, stats) is editable in **/admin → Site settings**

## Local development

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows  (source .venv/bin/activate on macOS/Linux)
pip install -r requirements.txt
copy .env.example .env          # then edit values
python manage.py migrate
python manage.py seed_site      # starter content
python manage.py createsuperuser
python manage.py runserver
```

Without `DATABASE_URL` it uses SQLite, without B2 it stores uploads in `media/`, and without Gmail
credentials emails are printed to the console.

Run tests: `python manage.py test`

## Deployment

### 1. PostgreSQL (free)
Create a database on **Neon** (neon.tech, also available from the Vercel Marketplace) or **Supabase**.
Copy the connection string into `DATABASE_URL` and set `DB_SSL_REQUIRE=True`.
Use the **pooled** connection string on Neon, because serverless functions open many short connections.
Both providers support the PostGIS extension if you later want maps or spatial data (`CREATE EXTENSION postgis;`).

### 2. Backblaze B2
1. Create a bucket (for example `little-harvard-media`) and set it to **Public**.
2. App Keys → *Add a New Application Key* with read/write access to that bucket.
3. Set `B2_BUCKET_NAME`, `B2_KEY_ID`, `B2_APPLICATION_KEY`, and `B2_ENDPOINT_URL` (shown on the bucket page,
   e.g. `https://s3.us-west-004.backblazeb2.com`) and `B2_REGION` (`us-west-004`).
4. Optional: put Cloudflare in front of B2 (free egress via the Bandwidth Alliance) and set `B2_CUSTOM_DOMAIN`.

### 3. Gmail SMTP
1. Turn on 2-Step Verification on the Google account.
2. Go to Google Account → Security → **App passwords** and create one for "Mail".
3. Set `EMAIL_HOST_USER=lilharvard5@gmail.com` and `EMAIL_HOST_PASSWORD=<16-char app password>`.
   Gmail allows roughly 500 emails a day, which is plenty for enquiries.

### 4. Google Analytics
Create a GA4 property and web stream, then set `GA_MEASUREMENT_ID=G-XXXXXXXXXX`.
The site sends `cta_click`, `phone_click`, `form_submit` and `generate_lead` (a completed application) events.
Mark `generate_lead` as a key event in GA.

### 5. Vercel
1. Push this folder to a GitHub repo and **Import** it in Vercel (Framework preset: *Other*).
2. Add the environment variables from `.env.example` (with `DEBUG=False`, a long random `SECRET_KEY`,
   `SITE_URL=https://your-domain`, and your domain in `ALLOWED_HOSTS` / `CSRF_TRUSTED_ORIGINS`).
3. Deploy. `build_files.sh` installs dependencies, runs `collectstatic` and `migrate`.
4. Once, from your machine pointed at the production DB: `python manage.py createsuperuser` and `python manage.py seed_site`.
5. Add a custom domain (e.g. `littleharvard.co.zw`) under Project → Domains. SSL is automatic.

**Serverless limits to know:** requests are capped at about 4.5 MB, so upload gallery photos 3–5 at a time
(they're resized automatically). The filesystem is read-only, which is why media must live on B2.

## Content to confirm with the school

The seed data uses facts from the school's public Facebook page (name, tagline, address, phone, email, hours).
Everything below is **placeholder content** to review in the admin before launch:

- Programme names, age ranges, timetables and **fees**
- Admission steps, requirements list and FAQs
- Mission, vision and values
- Staff profiles, real testimonials, homepage stats (hidden until filled in)
- Logo (upload the real logo in Site settings; the built-in SVG is a stand-in), hero and about photos
- Gallery albums: upload graduation and classroom photos; add Facebook reel links under Gallery → Videos
