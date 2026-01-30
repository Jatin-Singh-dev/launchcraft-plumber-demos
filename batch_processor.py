import csv
import json
import os
import shutil
import urllib.parse

# Config
CSV_PATH = 'briefs/batch/plumbers-batch2.csv'
BRIEFS_DIR = 'briefs/batch'
SITES_DIR = 'sites'
SOURCE_ASSETS = 'sites/citywide-plumbing/assets'

# -----------------------------------------------------------------------------
# 1. HTML TEMPLATE (Modern Mobile UI/UX)
# -----------------------------------------------------------------------------
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Plumbing {location} | Same-Day Service | {business_name}</title>
    <meta name="description" content="Professional Plumbing in {location}. Same-day service, upfront pricing, and satisfaction guaranteed. Call {business_name} at {phone} today!">
    <script type="application/ld+json">
    {{
      "@context": "https://schema.org",
      "@type": "PlumbingService",
      "name": "{business_name}",
      "telephone": "{phone}",
      "address": {{
        "@type": "PostalAddress",
        "addressLocality": "{city}",
        "addressRegion": "{state}"
      }},
      "areaServed": ["Dallas", "Fort Worth", "Arlington", "Plano", "Irving"],
      "openingHours": "Mon-Sun 00:00-24:00",
      "priceRange": "$$",
      "image": "assets/hero.webp"
    }}
    </script>
    <style>
        :root {{
            --primary: #0f3d2e;
            --accent: #a8ff2a;
            --light: #f4f4f4;
            --dark: #111;
            --text: #333;
            --white: #fff;
            --gray: #666;
            --border: #eee;
        }}
        * {{ box-sizing: border-box; }}
        body {{ margin: 0; font-family: system-ui, -apple-system, sans-serif; color: var(--text); line-height: 1.5; padding-top: 60px; }}
        a {{ text-decoration: none; color: inherit; transition: opacity 0.2s; }}
        img {{ max-width: 100%; height: auto; display: block; }}
        .container {{ max-width: 1200px; margin: 0 auto; padding: 0 20px; }}
        
        /* Typography */
        h1, h2, h3 {{ margin-top: 0; line-height: 1.2; color: var(--primary); }}
        
        /* BUTTONS */
        .btn {{ 
            display: inline-flex; justify-content: center; align-items: center;
            padding: 12px 24px; font-weight: 700; border-radius: 6px; 
            text-transform: uppercase; font-size: 0.95rem; border: none; cursor: pointer; text-align: center;
            transition: transform 0.2s;
        }}
        .btn:hover {{ transform: translateY(-2px); }}
        .btn-primary {{ background: var(--accent); color: var(--primary); }}
        .btn-secondary {{ background: transparent; border: 2px solid var(--accent); color: var(--white); }}
        .btn-full {{ width: 100%; }}
        
        /* 1) NAVBAR (Mobile & Desktop) */
        .navbar {{
            position: fixed; top: 0; left: 0; width: 100%; height: 60px;
            background: var(--white); border-bottom: 1px solid var(--border);
            z-index: 1000; display: flex; align-items: center; box-shadow: 0 2px 10px rgba(0,0,0,0.05);
        }}
        .nav-container {{ 
            width: 100%; max-width: 1200px; margin: 0 auto; padding: 0 20px;
            display: flex; justify-content: space-between; align-items: center;
        }}
        .brand {{ 
            font-size: 18px; font-weight: 700; color: var(--primary); 
            white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 80%;
        }}
        .hamburger {{ font-size: 24px; cursor: pointer; background: none; border: none; color: var(--primary); padding: 5px; }}
        
        .desktop-links {{ display: none; gap: 25px; font-weight: 600; font-size: 0.95rem; }}
        .desktop-phone {{ display: none; font-weight: 700; color: var(--primary); margin-left: 20px; }}

        /* Mobile Menu Overlay */
        .mobile-menu {{
            position: fixed; top: 60px; left: 0; width: 100%; background: var(--white);
            border-bottom: 1px solid var(--border); padding: 0; display: none;
            flex-direction: column; z-index: 999; box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        }}
        .mobile-menu a {{ padding: 15px 20px; border-bottom: 1px solid var(--border); font-weight: 600; color: var(--primary); }}
        .mobile-menu.active {{ display: flex; }}

        @media(min-width: 768px) {{
            .hamburger {{ display: none; }}
            .mobile-menu {{ display: none !important; }}
            .desktop-links {{ display: flex; align-items: center; }}
            .desktop-phone {{ display: block; }}
        }}

        /* 2) HERO */
        .hero {{ background: var(--primary); color: var(--white); padding: 40px 0 50px; overflow: hidden; }}
        .hero-grid {{ display: grid; gap: 20px; align-items: center; }}
        
        /* Hero Badge */
        .hero-badge {{ 
            display: inline-block; background: rgba(255,255,255,0.1); 
            color: var(--accent); padding: 5px 12px; border-radius: 50px; 
            font-size: 0.8rem; font-weight: 700; letter-spacing: 0.5px; margin-bottom: 10px; 
            border: 1px solid rgba(168, 255, 42, 0.3);
        }}
        
        .hero h1 {{ font-size: 1.8rem; margin-bottom: 10px; font-weight: 800; letter-spacing: -0.5px; color: var(--white); line-height: 1.1; }}
        .hero-sub {{ font-size: 1rem; margin-bottom: 20px; opacity: 0.9; line-height: 1.5; max-width: 500px; }}
        
        .hero-btns {{ display: flex; gap: 10px; flex-wrap: wrap; }}
        .hero-btns .btn {{ flex: 1; min-width: 130px; }}
        
        .hero-img img {{ border-radius: 8px; box-shadow: 0 10px 30px rgba(0,0,0,0.3); width: 100%; transform: rotate(1deg); }}
        
        @media(min-width: 768px) {{ 
            .hero {{ padding: 80px 0; }}
            .hero-grid {{ grid-template-columns: 1.1fr 0.9fr; gap: 60px; }} 
            .hero h1 {{ font-size: 3.2rem; margin-bottom: 15px; }} 
            .hero-btns .btn {{ flex: initial; width: auto; min-width: 180px; }}
            .hero-btns {{ justify-content: flex-start; }}
            .hero-sub {{ margin-bottom: 30px; font-size: 1.1rem; }}
        }}

        /* 3) TRUST BAR */
        .trust {{ padding: 25px 0; background: var(--light); text-align: center; border-bottom: 1px solid #e1e1e1; }}
        .trust-grid {{ display: flex; flex-wrap: wrap; justify-content: center; gap: 12px; }}
        .chip {{ 
            background: var(--white); padding: 8px 16px; border-radius: 50px; 
            font-weight: 600; box-shadow: 0 1px 3px rgba(0,0,0,0.05); 
            border: 1px solid #ddd; color: #555; font-size: 0.85rem; 
            display: flex; align-items: center; gap: 6px;
        }}

        /* 4) SERVICES */
        .services {{ padding: 60px 0; background: var(--white); }}
        .section-title {{ text-align: center; margin-bottom: 40px; color: var(--primary); font-size: 2rem; font-weight: 800; }}
        .services-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: 24px; }}
        .card {{ 
            padding: 25px; border-radius: 8px; box-shadow: 0 4px 12px rgba(0,0,0,0.05); 
            background: var(--white); border: 1px solid #eee; transition: transform 0.2s; 
        }}
        .card:hover {{ transform: translateY(-4px); border-color: var(--accent); }}
        .card h3 {{ color: var(--primary); margin-top: 0; font-size: 1.25rem; display: flex; align-items: center; gap: 10px; }}
        .card-icon {{ font-size: 1.5rem; }}

        /* 5) REVIEWS */
        .reviews {{ padding: 60px 0; background: var(--primary); color: var(--white); text-align: center; }}
        .stars {{ color: var(--accent); font-size: 1.3rem; margin-bottom: 8px; display: block; }}
        .review-grid {{ display: grid; grid-template-columns: 1fr; gap: 20px; margin-top: 30px; }}
        .review-card {{ background: rgba(255,255,255,0.05); padding: 20px; border-radius: 8px; text-align: left; border: 1px solid rgba(255,255,255,0.1); }}
        @media(min-width: 768px) {{ .review-grid {{ grid-template-columns: repeat(3, 1fr); }} }}

        /* 6) MAP */
        .map-section {{ padding: 60px 0; background: var(--light); }}
        iframe {{ width: 100%; height: 350px; border: 0; border-radius: 8px; display: block; box-shadow: 0 4px 12px rgba(0,0,0,0.1); }}

        /* 7) FAQ */
        .faq {{ padding: 60px 0; background: var(--white); }}
        .accordion-item {{ border-bottom: 1px solid #eee; padding: 18px 0; }}
        .accordion-title {{ font-weight: 600; cursor: pointer; display: flex; justify-content: space-between; font-size: 1.05rem; color: var(--primary); }}
        .accordion-content {{ display: none; margin-top: 12px; color: #555; line-height: 1.6; }}
        .accordion-item.active .accordion-content {{ display: block; }}
        .icon {{ color: var(--accent); font-weight: bold; font-size: 1.5rem; line-height: 0.8; }}

        /* 8) FORM */
        .contact {{ padding: 60px 0; background: var(--primary); }}
        .form-box {{ background: var(--white); color: var(--text); padding: 30px; border-radius: 8px; max-width: 500px; margin: 0 auto; box-shadow: 0 10px 30px rgba(0,0,0,0.2); }}
        .form-group {{ margin-bottom: 16px; }}
        .form-group label {{ display: block; margin-bottom: 6px; font-weight: 600; font-size: 0.9rem; }}
        .form-group input, .form-group select {{ width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 4px; font-size: 1rem; }}
        .success-msg {{ display: none; background: #e6fffa; color: #047857; padding: 12px; border-radius: 4px; text-align: center; margin-top: 15px; font-weight: 600; border: 1px solid #b2f5ea; }}

        /* 9) FOOTER */
        footer {{ background: #0b2d22; color: #999; padding: 40px 0; text-align: center; font-size: 0.9rem; border-top: 1px solid rgba(255,255,255,0.05); }}
        .footer-grid {{ display: grid; gap: 30px; text-align: left; max-width: 900px; margin: 0 auto 30px; }}
        .footer-col h4 {{ color: var(--white); margin-bottom: 15px; font-size: 1.1rem; }}
        .footer-col a {{ display: inline-block; margin-bottom: 5px; }}
        .footer-col a:hover {{ color: var(--accent); }}
        @media(min-width: 768px) {{ .footer-grid {{ grid-template-columns: 1fr 1fr; text-align: left; }} }}
        
        .highlight {{ color: var(--accent); }}
        
        /* Helpers */
        .mobile-only {{ display: block; }}
        .desktop-only {{ display: none; }}
        @media(min-width: 768px) {{ .mobile-only {{ display: none; }} .desktop-only {{ display: block; }} }}
    </style>
</head>
<body>

    <!-- NAVBAR -->
    <nav class="navbar">
        <div class="nav-container">
            <a href="#" class="brand">{business_name}</a>
            
            <!-- Desktop Nav -->
            <div class="desktop-links">
                <a href="#services">Services</a>
                <a href="#reviews">Reviews</a>
                <a href="#map">Areas</a>
                <a href="#faq">FAQ</a>
                <a href="#quote" style="background:var(--accent); padding:8px 16px; border-radius:4px; color:var(--primary);">Get Quote</a>
            </div>
            <a href="tel:{phone_clean}" class="desktop-phone">📞 {phone}</a>

            <!-- Mobile Burger -->
            <button class="hamburger" onclick="toggleNav()">☰</button>
        </div>
    </nav>

    <!-- MOBILE MENU -->
    <div class="mobile-menu" id="mobileMenu">
        <a href="#services" onclick="toggleNav()">Services</a>
        <a href="#reviews" onclick="toggleNav()">Reviews</a>
        <a href="#map" onclick="toggleNav()">Service Areas</a>
        <a href="#faq" onclick="toggleNav()">FAQ</a>
        <a href="#quote" onclick="toggleNav()" style="background: #f9f9f9;">Get Free Quote</a>
        <a href="tel:{phone_clean}" onclick="toggleNav()" style="color:var(--primary); font-weight:800;">📞 Call {phone}</a>
    </div>

    <!-- HERO -->
    <section class="hero">
        <div class="container hero-grid">
            <div class="hero-text">
                <div class="hero-badge">Plumbing Services in {location}</div>
                <h1>Professional Plumbing Services<br>in {city}, {state}</h1>
                <p class="hero-sub">Licensed, insured, and ready to help. Get top-rated local plumbing service today with same-day availability.</p>
                
                <div class="hero-btns">
                    <a href="tel:{phone_clean}" class="btn btn-primary btn-full">Call Now</a>
                    <a href="#quote" class="btn btn-secondary btn-full">Get Free Quote</a>
                </div>
            </div>
            <div class="hero-img">
                <!-- Using same image fallback logic -->
                <img src="assets/hero.webp" alt="Plumber in {location}" width="600" height="400" loading="eager" onerror="this.onerror=null; this.parentElement.style.background='#eee';">
            </div>
        </div>
    </section>

    <!-- TRUST BAR -->
    <section class="trust">
        <div class="container">
            <div class="trust-grid">
                <div class="chip">🛡️ Licensed & Insured</div>
                <div class="chip">⚡ Same-Day Service</div>
                <div class="chip">💰 Upfront Pricing</div>
                <div class="chip">🤝 Satisfaction Guaranteed</div>
            </div>
        </div>
    </section>

    <!-- SERVICES -->
    <section class="services" id="services">
        <div class="container">
            <h2 class="section-title">Our Services</h2>
            <div class="services-grid">
                <div class="card">
                    <h3><span class="card-icon">🚨</span> Emergency Plumbing</h3>
                    <p>Fast response for urgent plumbing needs.</p>
                </div>
                <div class="card">
                    <h3><span class="card-icon">🧹</span> Drain Cleaning</h3>
                    <p>Clear clogs and debris efficiently.</p>
                </div>
                <div class="card">
                    <h3><span class="card-icon">💧</span> Leak Repair</h3>
                    <p>Detect and fix leaks before damage worsens.</p>
                </div>
                <div class="card">
                    <h3><span class="card-icon">🔥</span> Water Heater Repair</h3>
                    <p>Installation and repair for all heater types.</p>
                </div>
                <div class="card">
                    <h3><span class="card-icon">🚽</span> Toilet Repair</h3>
                    <p>Fix running toilets and dripping faucets.</p>
                </div>
                <div class="card">
                    <h3><span class="card-icon">🔧</span> Pipe Replacement</h3>
                    <p>Professional re-piping services.</p>
                </div>
            </div>
        </div>
    </section>

    <!-- REVIEWS -->
    <section class="reviews" id="reviews">
        <div class="container">
            <h2 class="section-title" style="color:white; margin-bottom:10px;">What Neighbors Say</h2>
            <p style="margin-bottom:40px; opacity:0.9;">Rated 4.9/5 based on 50+ local reviews</p>
            
            <div class="review-grid">
                <div class="review-card">
                    <span class="stars">★★★★★</span>
                    <p>"{business_name} saved the day! They arrived within an hour and fixed our leak immediately. Highly recommended!"</p>
                    <p style="margin-top: 15px; font-weight: bold; font-size:0.9rem;">- Chris, {city}</p>
                </div>
                <div class="review-card">
                    <span class="stars">★★★★★</span>
                    <p>"Professional, clean, and upfront about the cost. No surprises. Will definitely use them again."</p>
                    <p style="margin-top: 15px; font-weight: bold; font-size:0.9rem;">- Taylor, {city}</p>
                </div>
                <div class="review-card">
                    <span class="stars">★★★★★</span>
                    <p>"Best plumbers in town. They installed our new water heater efficiently and took the old one away."</p>
                    <p style="margin-top: 15px; font-weight: bold; font-size:0.9rem;">- Jordan, {city}</p>
                </div>
            </div>
        </div>
    </section>

    <!-- MAP -->
    <section class="map-section" id="map">
        <div class="container">
            <h2 class="section-title">Serving {location}</h2>
            <p style="text-align:center; margin-bottom: 25px; font-size: 1.1rem; color:#666;">Serving Dallas, Fort Worth, Arlington, Plano, Irving & surrounding areas.</p>
            <iframe src="https://www.google.com/maps?q=Plumber+{url_location}&output=embed" allowfullscreen loading="lazy"></iframe>
        </div>
    </section>

    <!-- FAQ -->
    <section class="faq" id="faq">
        <div class="container">
            <h2 class="section-title">Frequently Asked Questions</h2>
            <div class="accordion">
                <div class="accordion-item">
                    <div class="accordion-title" onclick="toggleFaq(this)">Do you offer same-day service? <span class="icon">+</span></div>
                    <div class="accordion-content">Yes, we strive to offer same-day service for most calls, especially emergencies.</div>
                </div>
                <div class="accordion-item">
                    <div class="accordion-title" onclick="toggleFaq(this)">Are you licensed and insured? <span class="icon">+</span></div>
                    <div class="accordion-content">Absolutely. We are fully licensed and insured for your peace of mind.</div>
                </div>
                <div class="accordion-item">
                    <div class="accordion-title" onclick="toggleFaq(this)">Do you provide upfront pricing? <span class="icon">+</span></div>
                    <div class="accordion-content">Yes, we provide clear, upfront pricing before starting any work. No hidden fees.</div>
                </div>
                <div class="accordion-item">
                    <div class="accordion-title" onclick="toggleFaq(this)">What areas do you serve? <span class="icon">+</span></div>
                    <div class="accordion-content">We serve Dallas, Fort Worth, and all surrounding communities.</div>
                </div>
                <div class="accordion-item">
                    <div class="accordion-title" onclick="toggleFaq(this)">How do I get a quote? <span class="icon">+</span></div>
                    <div class="accordion-content">You can call us directly or use the form below to request a free quote.</div>
                </div>
            </div>
        </div>
    </section>

    <!-- FORM -->
    <section class="contact" id="quote">
        <div class="container">
            <h2 class="section-title" style="color:white; margin-bottom:10px;">Get A Free Quote</h2>
            <p style="text-align:center; color:white; margin-bottom:40px; opacity:0.9;">Tell us what you need and we'll call you back shortly.</p>
            <div class="form-box">
                <form onsubmit="event.preventDefault(); document.querySelector('.success-msg').style.display='block'; this.reset();">
                    <div class="form-group">
                        <label>Name</label>
                        <input type="text" required placeholder="Your Name">
                    </div>
                    <div class="form-group">
                        <label>Phone</label>
                        <input type="tel" required placeholder="Your Phone Number">
                    </div>
                    <div class="form-group">
                        <label>Service Needed</label>
                        <select>
                            <option>Emergency Plumbing</option>
                            <option>Drain Cleaning</option>
                            <option>Leak Repair</option>
                            <option>Water Heater Repair</option>
                            <option>Other</option>
                        </select>
                    </div>
                    <p style="margin-bottom:15px; font-weight:600; font-size:0.9rem;">Or call: <a href="tel:{phone_clean}" style="color:var(--primary);">{phone}</a></p>
                    <button type="submit" class="btn btn-primary btn-full">Request Quote</button>
                    <div class="success-msg">Thanks! We’ll call you back within 10 minutes.</div>
                </form>
            </div>
        </div>
    </section>

    <!-- FOOTER -->
    <footer>
        <div class="container">
            <div class="footer-grid">
                <div class="footer-col">
                    <h4 style="color:var(--white);">{business_name}</h4>
                    <p>Professional plumbing services in {location}.</p>
                    <p style="margin-top:10px;"><strong>Phone:</strong> <a href="tel:{phone_clean}" style="color:var(--accent);">{phone}</a></p>
                </div>
                <div class="footer-col">
                    <h4 style="color:var(--white);">Links</h4>
                    <a href="#services">Services</a><br>
                    <a href="#quote">Get Quote</a><br>
                    <a href="#map">Service Areas</a>
                </div>
                <div class="footer-col">
                    <h4 style="color:var(--white);">Hours</h4>
                    <p>Mon–Sun: Open 24 Hours</p>
                </div>
            </div>
            <p style="margin-top: 30px; opacity: 0.5; font-size:0.8rem;">This is a demo site. For emergencies call immediately.</p>
        </div>
    </footer>

    <script>
        function toggleNav() {{
            var menu = document.getElementById('mobileMenu');
            menu.classList.toggle('active');
        }}

        function toggleFaq(el) {{
            const item = el.parentElement;
            const content = item.querySelector('.accordion-content');
            const wasActive = item.classList.contains('active');
            
            document.querySelectorAll('.accordion-item').forEach(i => {{
                i.classList.remove('active');
                i.querySelector('.icon').innerText = '+';
            }});

            if (!wasActive) {{
                item.classList.add('active');
                el.querySelector('.icon').innerText = '-';
            }}
        }}
    </script>
</body>
</html>"""

# -----------------------------------------------------------------------------
# 2. DIRECTORY TEMPLATE
# -----------------------------------------------------------------------------
DIRECTORY_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Generated Sites Directory</title>
    <style>
        body {{ font-family: system-ui; max-width: 800px; margin: 40px auto; padding: 0 20px; background: #f4f4f4; }}
        h1 {{ text-align: center; color: #333; }}
        input {{ width: 100%; padding: 15px; font-size: 1.1rem; margin-bottom: 30px; border: 1px solid #ddd; border-radius: 5px; box-sizing:border-box; }}
        .list {{ display: grid; gap: 15px; }}
        .item {{ background: #fff; padding: 20px; border-radius: 8px; text-decoration: none; color: #333; display: block; box-shadow: 0 2px 5px rgba(0,0,0,0.05); transition: transform 0.2s; }}
        .item:hover {{ transform: translateY(-3px); box-shadow: 0 5px 15px rgba(0,0,0,0.1); }}
        .item h3 {{ margin: 0 0 5px; color: #0f3d2e; }}
        .item p {{ margin: 0; color: #666; font-size: 0.9rem; }}
    </style>
</head>
<body>
    <h1>Generated Plumbing Sites</h1>
    <input type="text" id="search" placeholder="Search businesses..." onkeyup="filter()">
    <div class="list" id="list">
        {links}
    </div>
    <script>
        function filter() {{
            const q = document.getElementById('search').value.toLowerCase();
            document.querySelectorAll('.item').forEach(el => {{
                el.style.display = el.innerText.toLowerCase().includes(q) ? 'block' : 'none';
            }});
        }}
    </script>
</body>
</html>"""

# -----------------------------------------------------------------------------
# 3. README TEMPLATE
# -----------------------------------------------------------------------------
README_TEMPLATE = """# {business_name} Landing Page

## Overview
This is a high-converting, mobile-first landing page generated for **{business_name}** in **{location}**.

## Features
-   **Modern Mobile UI**: Burger menu, polished hero section, and optimized typography.
-   **Speed**: Pure HTML/CSS, no frameworks, <150KB target.
-   **SEO**: Schema markup, meta tags, and optimized content structure.

## Quick Start
1.  Open `index.html` in your browser to preview.
2.  Images are loaded from the `assets/` folder.

## Assets
Ensure the following files exist in `assets/`:
-   `hero.webp` (Max 1200px)
-   `team.webp`
-   `before-after-1.webp`
-   `before-after-2.webp`

## Deployment
This folder is ready to deploy to Netlify, Cloudflare Pages, or Vercel. 
Just drag and drop the folder!
"""

# -----------------------------------------------------------------------------
# UTILS
# -----------------------------------------------------------------------------
def clean_phone(p):
    return p.replace(' ', '').replace('-', '').replace('(', '').replace(')', '')

def parse_location(loc):
    parts = loc.split(',')
    if len(parts) >= 2:
        return parts[0].strip(), parts[1].strip()
    return loc, "TX"

# -----------------------------------------------------------------------------
# MAIN RUN
# -----------------------------------------------------------------------------
def run():
    if not os.path.exists(BRIEFS_DIR):
        os.makedirs(BRIEFS_DIR, exist_ok=True)

    generated_sites = []

    with open(CSV_PATH, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            slug = row['slug'].strip()
            biz_name = row['business_name'].strip()
            loc = row['location'].strip()
            phone = row['phone'].strip()
            
            # 1. JSON Brief
            brief = {
                "slug": slug,
                "business_name": biz_name,
                "industry": "Plumbing",
                "location": loc,
                "primary_goal": "calls",
                "offer": "Same-day service. Upfront pricing. No surprises.",
                "phone": phone,
                "services": ["Emergency Plumbing", "Drain Cleaning", "Leak Repair", "Water Heater Repair", "Toilet & Faucet Repair", "Pipe Replacement"],
                "brand": {"primary_color": "#0f3d2e", "accent_color": "#a8ff2a"},
                "images": {"hero": "assets/hero.webp", "team": "assets/team.webp", "before_after_1": "assets/before-after-1.webp", "before_after_2": "assets/before-after-2.webp"}
            }
            
            with open(os.path.join(BRIEFS_DIR, f"{slug}.json"), 'w', encoding='utf-8') as jf:
                json.dump(brief, jf, indent=2)
                
            # 2. Site Directories & Assets
            site_path = os.path.join(SITES_DIR, slug)
            assets_path = os.path.join(site_path, 'assets')
            
            if not os.path.exists(assets_path):
                os.makedirs(assets_path, exist_ok=True)
                
            # Copy assets if source exists
            if os.path.exists(SOURCE_ASSETS):
                for item in os.listdir(SOURCE_ASSETS):
                    s = os.path.join(SOURCE_ASSETS, item)
                    d = os.path.join(assets_path, item)
                    if os.path.isfile(s):
                        shutil.copy2(s, d)

            # 3. Generate HTML
            city, state = parse_location(loc)
            phone_clean = clean_phone(phone)
            url_location = loc.replace(' ', '+').replace('–', '-') # handle en-dash
            
            # Populate HTML template
            html_content = HTML_TEMPLATE.format(
                business_name=biz_name,
                location=loc,
                phone=phone,
                phone_clean=phone_clean,
                city=city,
                state=state,
                url_location=url_location
            )
            
            # Write index.html
            with open(os.path.join(site_path, 'index.html'), 'w', encoding='utf-8') as hf:
                hf.write(html_content)

            # Write README.md
            readme_content = README_TEMPLATE.format(business_name=biz_name, location=loc)
            with open(os.path.join(site_path, 'README.md'), 'w', encoding='utf-8') as rf:
                rf.write(readme_content)
                
            print(f"Generated site: {slug}")
            generated_sites.append({"name": biz_name, "slug": slug, "loc": loc})

    # 4. Generate Directory Page
    links_html = ""
    for s in generated_sites:
        links_html += f'<a href="{s["slug"]}/index.html" class="item"><h3>{s["name"]}</h3><p>{s["loc"]}</p></a>\n'
    
    directory_html = DIRECTORY_TEMPLATE.format(links=links_html)
    with open(os.path.join(SITES_DIR, 'index.html'), 'w', encoding='utf-8') as df:
        df.write(directory_html)
        
    print(f"Generated directory page with {len(generated_sites)} sites.")

if __name__ == '__main__':
    run()
