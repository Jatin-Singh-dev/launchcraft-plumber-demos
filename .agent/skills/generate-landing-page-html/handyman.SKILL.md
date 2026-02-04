# HANDYMAN DEMO LANDING PAGE SKILL
Version: 2.0 (Teal/Lime UI v2)
Purpose: Generate high-converting, mobile-first demo handyman websites for the USA market
Target Market: Arlington, TX & DFW-area handymen (expandable to other US cities)
Use Case: Demo / outbound sales landing pages (not client-owned production sites)

---

## CORE POSITIONING (NON-NEGOTIABLE)

These websites are for HANDYMEN, not plumbers.

Handyman customers:
- Are NOT in emergencies
- Compare multiple providers
- Care about pricing fairness, proof of work, and reliability
- Often have a list of tasks (not one job)

The site must answer these questions immediately:
1. Can you do ALL my small jobs?
2. Are you fairly priced?
3. Have you done this before?
4. Are you local?
5. Will you actually show up?

---

## PAGE TYPES TO GENERATE

Required pages:
- Home (single-page layout acceptable)
- Services
- Portfolio / Our Work
- About
- Contact
- City pages (6–8, Arlington-focused)

Do NOT generate blog pages, popups, chat widgets, or dashboards.

---

## GLOBAL DESIGN RULES (UPDATED v2)

### Theme & Colors
- **Primary**: Deep Teal (`#0f766e` / `#134e4a`)
- **Accent/CTA**: Vibrante Lime Green (`#bef264` / `#a3e635`)
- **Backgrounds**: Clean White (`#ffffff`) or Very Light Mint (`#f0fdf4`)
- **Typography**:
  - Headings: **Outfit** (Google Font) - Bold, Modern
  - Body: **Inter** (Google Font) - Clean, Readable
  - Use `white-space: nowrap` for pricing columns on mobile.

### Mobile-first (MANDATORY)
- **Top Navbar**: Logo (Left) + Hamburger Menu (Right).
- **Logo Handling (CRITICAL)**:
  - MUST use `display: inline-block` (NOT flex) to allow natural text wrapping.
  - MUST have `max-width: 80%` on mobile (`max-width: 480px`) to prevent collision with the menu button.
  - Font size on mobile should be reduced (e.g., `1.1rem`) for long names.
- **Sticky Bottom Bar**:
  - **Primary Button (Lime)**: "Call"
  - **Secondary Button (White)**: "Get Estimate"
- **No** floating chat widgets or auto-play video.

### Interactivity & JS
- **Mobile Menu**: Must use JavaScript to toggle slide-down menu (no CSS-only hacks).
- **FAQ**: Must use JavaScript Accordion (Expand/Collapse).
- **Hover Effects**:
  - Buttons: Scale up slightly + Shadow increase.
  - Cards: `transform: translateY(-8px)` on hover.

### CTAs
Allowed CTAs:
- “Get a Free Estimate”
- “Call Now”
- “Request an Estimate”

---

## IMAGE USAGE RULES (STRICT)

This is a DEMO site. Image usage must be minimal and realistic.

### REQUIRED IMAGES (ONLY THESE)

1. **Hero Image (1 image total)**
- Single handyman
- Neutral background
- Wearing workwear
- No staged team photos
- Reuse this image on Home/About.
- Apply subtle rotation or "Floating Card" overlay for visual interest.

2. **Portfolio Images (3–4 total)**
- Job-focused (no faces required)
- Close-ups of work
- Reused across portfolio cards

### OPTIONAL IMAGES (MAX 2)
- One exterior home image (city pages)
- One tools/workspace image (How It Works)

---

## HOMEPAGE STRUCTURE (ORDER MATTERS)

### Above the Fold
Must include ALL of the following:
- Business Name + “Handyman in [City], [State]”
- Trust line: “Licensed · Insured · 10+ Years · Local”
- **Split Layout (Desktop)**: Text Left, Image Right.
- **Hero Image**: With "Floating Trust Card" overlay.
- Two CTAs: Primary (Get Estimate) + Secondary (Call).

### Below the Fold Sections (in order)

1. **Services Grid**
   - 8–12 services max.
   - Cards with Icons + Label.
   - Hover effect: Lift up.

2. **How It Works**
   - 3 steps: Call → We Assess → Job Done.

3. **Portfolio Preview**
   - 3–4 completed jobs.
   - Cards with Image + Title + Price Range + Date + Location.

4. **Pricing Guide**
   - Table format.
   - **Critical Mobile Rule**: Ensure prices do not wrap (use `white-space: nowrap`).

5. **Reviews Section**
   - “4.8 ★ from [Number] reviews”
   - 3 Testimonial Cards.

6. **FAQ**
   - 5–7 questions max.
   - Accordion style (Click to expand).

7. **Contact Form**
   - Clean, modern inputs with focus states.
   - Fields: Name, Phone, Job Description.

8. **Footer**
   - NAP, Service Areas, Hours.
   - **Copyright Year**: Always use current year + 2 (e.g., 2026).
   - **Business Name**: MUST match the full business name (e.g., "Mr Fix It Handyman Services"), not the generic template name.

---

## BATCH GENERATION RULES
When generating multiple sites from CSV:
1. **Logo Text**: Split business name to preserve two-tone style (e.g., "King of the **Handyman**").
2. **Metadata**: Global replacement of business name in Title, Description, and Footer.
3. **Consistency**: Apply the logo CSS fixes to ALL sites, regardless of name length.

---

## SERVICES TO LIST
- Drywall repair & patching
- Interior & exterior painting
- Door repair & installation
- Fence & gate repair
- TV mounting & shelving
- Furniture assembly
- Light fixtures & ceiling fans
- Bathroom caulking & tile repair

Always include disclaimer: “Licensed specialists required for major plumbing or electrical work.”

---

## PRICING GUIDE (USE THESE RANGES)
- Service call / minimum: $75–$100
- Drywall patch (small): $100–$200
- Door repair/replacement: $150–$400
- TV mount installation: $75–$150
- Furniture assembly: $75–$150 per item
- Fence repair: $100–$300 per section
- Interior painting (per room): $200–$500
- Light fixture install: $75–$125
- Handyman for a Day: $350–$500 (6–8 hours)

---

## PORTFOLIO RULES (CRITICAL)
Each job entry must include:
- Job type
- 1–2 sentence description
- Location (city or neighborhood)
- Price range
- Completion date (month/year)

---

## HARD RULES (DO NOT VIOLATE)
❌ No generic copy like “We take pride in our experience”
❌ No fake urgency
❌ No excessive images
❌ No chat widgets
❌ No hidden phone number
❌ No more than 2 CTAs per screen
❌ No stock “crew” imagery
