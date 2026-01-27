---
name: generate-landing-page-html
description: Generate an ultra-fast, high-converting blue-collar (plumber/HVAC/electrician) single-file landing page from /briefs/*.json in LaunchCraft style, with image support, sticky click-to-call, map, FAQ, and short quote form.
---

# PRIMARY GOAL
Create a FAST (<2s mobile), mobile-first landing page that maximises PHONE CALLS and quote requests for blue-collar local service businesses (plumbers, HVAC, electricians). This must feel like a proven converting local service site: big phone, urgency, trust, and frictionless contact.

# INPUT (JSON)
Path: /briefs/<slug>.json

## REQUIRED FIELDS
- slug (string)
- business_name (string)
- industry (string) e.g. "Plumbing"
- location (string) e.g. "Austin, TX"
- primary_goal (string) e.g. "calls"
- offer (string)
- phone (string)
- services (array of strings OR array of objects)
- brand.primary_color (hex)
- brand.accent_color (hex)

## SERVICES FORMAT
services can be:

Option A:
["Emergency Plumbing", "Drain Cleaning"]

Option B:
[
  { "name": "Emergency Plumbing", "one_liner": "Fast response", "price_hint": "From $99" }
]

Rules:
- Show name always
- Show one_liner if provided
- price_hint optional
- If more than 6 services → render best 6

## OPTIONAL FIELDS (HIGHLY RECOMMENDED)
- rating
- review_count
- years_in_business
- badges (array)
- hours
- service_areas (array)
- emergency (boolean)
- faq (array of {q,a})
- testimonials (array of {name, area, text})
- form.service_needed_options (array)
- map.query (string)
- map.embed_url (string)

## IMAGES OBJECT (OPTIONAL)
Paths relative to site folder:

{
  "hero": "assets/hero.webp",
  "team": "assets/team.webp",
  "before_after_1": "assets/before-after-1.webp",
  "before_after_2": "assets/before-after-2.webp"
}

# OUTPUT (FILES/FOLDERS)
Create:

/sites/<slug>/
- index.html
- README.md
- assets/ (always)

# SPEED OPTIMISATION RULES (NON-NEGOTIABLE)
- No frameworks
- No external libraries
- No jQuery
- Inline CSS only
- Minimal vanilla JS (FAQ + form success only)
- System fonts only
- No video
- No sliders
- Images:
  - WebP preferred
  - Hero ≤1200px width
  - <150KB target
  - loading="lazy" except hero
  - decoding="async"
  - width + height attributes

# CONVERSION BLUEPRINT

## 1) STICKY CLICK-TO-CALL (ALWAYS)
- Header phone link
- Floating call button:
  - Mobile bottom fixed
  - Desktop bottom-right
  - tel: link
  - accent color
  - ≥48px height
- If emergency=true show "Emergency?"

## 2) HERO
H1:
Professional <industry> in <location>

Subheadline:
Licensed + Insured + years + Same-day

3 bullets:
- Fast response
- Upfront pricing
- Satisfaction guaranteed

CTAs:
- CALL NOW (tel)
- GET FREE QUOTE (scroll)

Hero image right desktop / below mobile

## 3) TRUST BAR
4 chips:
- Licensed & Insured
- Same-day / Emergency
- Upfront Pricing
- Satisfaction Guaranteed

Use badges if provided else defaults.

## 4) SERVICES
4–6 cards
Icon + name + one-liner

## 5) SOCIAL PROOF
Rating line:
<rating>★ from <review_count> Google Reviews

Defaults:
4.9★ from 50+ Google Reviews

2–3 testimonials (generate if missing)

## 6) SERVICE AREA + MAP (REQUIRED)
Text:
service_areas OR "Serving <location> & surrounding areas"

Map iframe:
If map.embed_url use it
Else:
https://www.google.com/maps?q=<encoded(query||location)>&output=embed

Responsive + lazy loaded

## 7) FAQ (REQUIRED)
5–7 items

Defaults:
- Same-day service?
- Licensed & insured?
- Upfront pricing?
- Areas served?
- Emergencies?
- How to get quote?

Accordion:
CSS + tiny JS allowed
First open desktop ok

## 8) QUOTE FORM (REQUIRED)
Fields:
- Name (required)
- Phone (required)
- Service Needed (select)

Inline success:
"Thanks! We’ll call you back within 10 minutes."

Show phone near form.

No backend.

## 9) FOOTER
Show:
- business_name
- phone
- hours
- service areas
- trust text

Include:
"This is a demo site. For emergencies call immediately."

# SEO REQUIREMENTS
- One H1 only
- H2 sections:
  Services
  Reviews
  Service Areas
  FAQ
  Get a Free Quote

Title:
<industry> <location> | Same-Day Service | <business_name>

Meta description:
Include industry + location + CTA + phone

Alt text:
service + location

# SCHEMA MARKUP (REQUIRED)
JSON-LD LocalBusiness

Rules:
- type = Plumber if industry contains "plumb" else LocalBusiness
- name
- telephone
- url placeholder
- addressLocality + region from location
- openingHours if provided
- areaServed

# VISUAL STYLE
- primary_color background (deep green)
- accent_color for CTAs (neon lime)
- White cards
- Rounded corners
- Soft shadows
- Mobile first
- High contrast typography

# REQUIRED PAGE ORDER
0 Floating call button
1 Header
2 Hero
3 Trust bar
4 Services
5 Reviews
6 Service area + map
7 FAQ
8 Quote form
9 Footer

# IMAGE HANDLING (BATCH SAFE)
Always:

- Create /assets folder
- If images missing, assume:
  assets/hero.webp
  assets/team.webp
  assets/before-after-1.webp
  assets/before-after-2.webp

Always render:
- Hero image
- Team section image
- Before/after section (2 images)

If file missing:
Render placeholder card:
"Add hero.webp to /assets"

# README.md MUST INCLUDE
- How to preview locally (open index.html)
- Required image filenames
- How to convert to WebP (Squoosh)
- Hero width recommendation
- Cloudflare Pages deploy steps
- How to duplicate for new client

# BATCH GENERATION COMPATIBILITY
Must work when:
- JSON auto-generated from CSV
- services are strings
- images missing
- faq missing
- testimonials missing
- map missing

Defaults must be generated.
No failures allowed.

# HARD DO NOT
- No popups
- No chat widgets
- No external JS
- No Google Fonts
- No videos
- No sliders
- No heavy animations
