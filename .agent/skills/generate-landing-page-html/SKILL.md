---
name: generate-landing-page-html
description: Generate ultra-fast, high-converting blue-collar single-file landing pages from /briefs/*.json in LaunchCraft style. Includes proper mobile sticky call bar, trust, map, FAQ, short quote form, image support, and directory index.
---

# PRIMARY GOAL
Create FAST (<2s mobile), mobile-first landing pages that maximise PHONE CALLS and quote requests for local blue-collar service businesses (plumbing/HVAC/electrician). Must feel like a proven converting local service site: big phone, urgency, trust, and frictionless contact.

# INPUT (JSON)
Path: /briefs/<slug>.json

## REQUIRED FIELDS
- slug (string)
- business_name (string)
- industry (string) e.g. "Plumbing"
- location (string) e.g. "Austin, TX"
- primary_goal (string) e.g. "calls"
- offer (string) short promise/offer
- phone (string) phone number shown everywhere
- services (array of strings OR array of objects with name/one_liner/price_hint)
- brand.primary_color (hex)
- brand.accent_color (hex)

## OPTIONAL FIELDS (HIGHLY RECOMMENDED)
- rating (string/number) e.g. "4.9"
- review_count (string/number) e.g. "47"
- years_in_business (string) e.g. "10+"
- badges (array of strings) e.g. ["Licensed & Insured", "Same-Day Service", "Upfront Pricing", "Warranty Included"]
- hours (string) e.g. "Mon–Sat 8:00 AM – 6:00 PM"
- service_areas (array of strings) e.g. ["Downtown", "Round Rock", ...]
- emergency (boolean) if true emphasize emergency messaging
- faq (array of {q,a}) up to 7 items
- testimonials (array of {name, area, text}) 2–3 items
- form.service_needed_options (array of strings) otherwise derive from services
- map.query (string) e.g. "Plumber Austin TX" OR map.embed_url (string)
- images (object with paths relative to site folder), e.g.:
  {
    "hero": "assets/hero.webp",
    "team": "assets/team.webp",
    "before_after_1": "assets/before-after-1.webp",
    "before_after_2": "assets/before-after-2.webp"
  }

# HARD RULE: NO HALLUCINATED BUSINESS DATA
- business_name MUST come from the brief only.
- Do NOT invent owner names, founder names, license numbers, or company history not present in the brief.
- Testimonials:
  - If not provided, generate placeholders BUT do not use real-sounding identifiable names like “Andersen” etc.
  - Use neutral first names only: “Chris”, “Taylor”, “Jordan”, “Sam”, “Alex” + area. (No last names.)

# OUTPUT (FILES/FOLDERS TO CREATE)
Create: /sites/<slug>/
- index.html  (SINGLE FILE, inline CSS, minimal JS only if needed for FAQ toggle and form success message)
- README.md   (preview/deploy instructions)
- assets/     (ALWAYS create this folder even if empty)

ALSO create a directory page at:
- /sites/index.html  (lists links to all /sites/<slug>/ pages)

# SPEED OPTIMISATION RULES (NON-NEGOTIABLE)
- NO frameworks, NO build steps
- NO external libraries (no jQuery)
- Plain HTML/CSS. Tiny vanilla JS allowed only for:
  - FAQ accordion toggle
  - form success message
- Inline critical CSS in <style>
- Use system fonts only (no Google Fonts)
- Avoid heavy animations, popups, sliders, and video backgrounds
- Images:
  - Prefer WebP
  - Hero max 1200px width
  - Target <150KB per image
  - loading="lazy" for all non-hero images (hero can be eager)
  - decoding="async"
  - Add width/height attributes when possible

# CONVERSION BLUEPRINT (MUST IMPLEMENT)

## 1) NAVBAR (MOBILE + DESKTOP)
- **Universal Fixed Navbar** (White background, shadow).
- **Mobile Layout**:
  - Left: proper **business_name** (Logo style, bold, 18-20px text).
  - Right: **Hamburger Menu Icon (☰)** (toggles nav links).
  - **NO** top "Call Now" strip. **NO** floating headers.
- **Desktop Layout**:
  - Logo Left.
  - Links Center (Services, Reviews, Areas, FAQ, Quote).
  - Phone Number Right (Text + Icon).

## 2) HERO ABOVE THE FOLD (MOBILE OPTIMISED)
- **Background**: Deep primary color.
- **Text Color**: **White** (H1 must be white/light to be visible).
- **Elements Order**:
  1.  **Service Badge/Pill**: "Plumbing Services in <Location>" (Capsule style, accent border).
  2.  **H1**: "Professional <industry> in <location>" (2-3 lines max, big font).
  3.  **Subheadline**: 1-2 lines intro text.
  4.  **Dual CTAs**:
      -   **Primary**: "CALL NOW" (Pro color, full width or flex).
      -   **Secondary**: "GET FREE QUOTE" (Outline style).
- **Spacing**:
  - Top padding: Compact (40-50px).
  - **NO** massive whitespace gaps.
  - Tighter margins between H1 and buttons.

## 3) TRUST BAR
Show 4 trust chips/cards:
- Licensed & Insured
- Same-Day / Emergency (if emergency=true)
- Upfront Pricing
- Satisfaction Guarantee / Warranty

## 5) SERVICES
- 4–6 service cards max.
- Each: icon/emoji, name, one-liner
- If >6 given, choose the best 6.

## 6) SOCIAL PROOF
- Show:
  "<rating>★ from <review_count> Google Reviews"
- If missing: default to "4.9★ from 50+ Google Reviews" (placeholder)
- Testimonials:
  - If brief provided, use them exactly.
  - If missing: generate 2–3 short placeholders with neutral first names only (no last names).

## 7) SERVICE AREAS + MAP (REQUIRED)
- List of areas served:
  - Use service_areas if present
  - Else "Serving <location> & surrounding areas"
- Embedded map:
  - Use map.embed_url if provided
  - Else use:
    src="https://www.google.com/maps?q=<ENCODED_QUERY>&output=embed"
- iframe must be responsive and loading="lazy"

## 8) FAQ (REQUIRED)
- 5–7 FAQs.
- Use brief faq if provided else generate common ones.
- Simple accordion:
  - works without heavy JS
  - tiny JS allowed
  - default open: first item open on desktop, collapsed on mobile is fine

## 9) QUOTE FORM (REQUIRED, SHORT)
- Must be visible and easy to find.
- Required fields:
  - Name (text)
  - Phone (tel)
  - Service Needed (select)
- Optional: message textarea
- Submit shows inline success message:
  "Thanks! We’ll call you back within 10 minutes."
- Repeat phone number near form for call-first users
- No backend required by default (unless explicitly requested)

## 10) FOOTER
- Repeat: phone, hours, service area, trust text
- Disclaimer:
  "For emergencies, call immediately."
- If years_in_business present, show it.

# SEO REQUIREMENTS (MUST IMPLEMENT)
- <title> = "<industry> <location> | Same-Day Service | <business_name>"
- meta description includes service + location + CTA + phone (150–160 chars)
- One H1 only
- H2s: Services, Reviews, Service Areas, FAQ, Get a Free Quote
- Image alt text includes service + location when appropriate

## SCHEMA MARKUP (JSON-LD) REQUIRED
Add LocalBusiness schema:
- @type: "Plumber" if industry contains "plumb", else "LocalBusiness"
- name, telephone, url (placeholder), addressLocality/Region from location if possible
- openingHours (if hours provided, approximate)
- areaServed (service_areas if present)

# VISUAL STYLE (LaunchCraft)
- Use brand.primary_color as deep primary background
- Use brand.accent_color for CTAs/highlights
- White/light cards/sections for contrast
- Rounded corners, soft shadows
- Bold, high-contrast typography
- Clean spacing, scannable mobile layout

# REQUIRED PAGE ORDER (STRICT)
0) Navbar (Mobile + Desktop)
1) Hero
2) Trust bar
3) Services grid
4) Reviews/testimonials
5) Service areas + map
6) FAQ
7) Quote form
8) Footer

# IMAGE HANDLING (REQUIRED)
- ALWAYS create /sites/<slug>/assets/
- If images.* exists, render <img>
- If missing, render a styled placeholder box:
  "Add hero.webp to /assets"

Standard filenames:
- assets/hero.webp
- assets/team.webp
- assets/before-after-1.webp
- assets/before-after-2.webp

# DIRECTORY PAGE (REQUIRED)
Create /sites/index.html which:
- lists all generated sites as clickable links
- shows business_name + industry + location
- includes a search input (optional tiny JS) to filter list
- is clean, simple, fast

# README.md MUST INCLUDE
- How to preview locally (open index.html)
- Where to place images (exact filenames)
- How to convert images to WebP (Squoosh, width 1200 hero)
- Cloudflare Pages deployment tips
- How to duplicate for a new demo (copy folder + update brief)

# HARD "DO NOT" LIST
- No popups
- No chat widgets
- No video backgrounds
- No heavy animations
- No multiple font downloads
- No external JS libraries
