import csv
import json
import os
import shutil
import urllib.parse

# Config
CSV_PATH = 'briefs/plumbers-batch.csv'
BRIEFS_DIR = 'briefs/batch'
SITES_DIR = 'sites'
SOURCE_ASSETS = 'sites/citywide-plumbing/assets'

# -----------------------------------------------------------------------------
# 1. HTML TEMPLATE (Metroflow UI Alignment)
# -----------------------------------------------------------------------------
HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Plumbing Services in {location} | Same-Day Service | {business_name}</title>
    <meta name="description" content="Professional Plumbing Services in {location}. Same-day service, upfront pricing, and guaranteed workmanship. Call {business_name} at {phone} today!">
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
      "areaServed": ["{city}", "Houston", "Sugar Land", "The Woodlands", "Katy"],
      "openingHours": "Mon-Sun 00:00-24:00",
      "priceRange": "$$",
      "image": "assets/hero.webp"
    }}
    </script>
    <style>
        :root {{
            --primary: #0b3d2e;
            --accent: #b7ff3c;
            --light: #f9fafb;
            --dark: #111;
            --text: #333;
            --white: #fff;
            --border: #e5e7eb;
            --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        }}

        * {{ box-sizing: border-box; }}
        html {{ scroll-behavior: smooth; }}
        body {{ 
            margin: 0; 
            font-family: system-ui, -apple-system, sans-serif; 
            color: var(--text); 
            line-height: 1.5; 
            background: var(--light);
            padding-top: 60px;
        }}

        a {{ text-decoration: none; color: inherit; }}
        img {{ max-width: 100%; height: auto; display: block; }}
        .container {{ max-width: 1200px; margin: 0 auto; padding: 0 20px; }}

        /* Buttons */
        .btn {{
            display: inline-flex; justify-content: center; align-items: center;
            padding: 14px 28px; font-weight: 700; border-radius: 8px;
            text-transform: uppercase; font-size: 0.9rem; border: none; cursor: pointer;
            transition: all 0.2s; min-height: 48px; text-align: center;
            flex: 1; min-width: 160px;
        }}
        .btn-primary {{ background: var(--accent); color: var(--primary); }}
        .btn-primary:hover {{ background: #a5e636; transform: translateY(-2px); }}
        .btn-outline {{ 
            background: transparent; border: 2px solid var(--accent); color: var(--white); 
        }}
        .btn-outline:hover {{ background: rgba(183, 255, 60, 0.1); transform: translateY(-2px); }}
        .btn-full {{ width: 100%; flex: auto; }}

        /* Navbar */
        .navbar {{
            position: fixed; top: 0; left: 0; width: 100%; height: 60px;
            background: var(--white); border-bottom: 1px solid var(--border);
            z-index: 1000; transition: box-shadow 0.3s;
        }}
        .navbar.scrolled {{ box-shadow: var(--shadow); }}
        .nav-container {{
            height: 100% !important; display: flex; justify-content: space-between; align-items: center;
        }}
        .brand {{ font-size: 18px; font-weight: 800; color: var(--primary); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; max-width: 80%; }}
        .hamburger {{ 
            font-size: 24px; background: none; border: none; cursor: pointer; color: var(--primary); padding: 5px; 
        }}

        /* Slide-down Menu */
        .nav-menu {{
            position: absolute; top: 60px; left: 0; width: 100%; background: var(--white);
            display: none; flex-direction: column; border-bottom: 1px solid var(--border);
            box-shadow: var(--shadow);
        }}
        .nav-menu.active {{ display: flex; }}
        .nav-menu a {{ padding: 18px 20px; border-top: 1px solid var(--border); font-weight: 600; color: var(--primary); font-size: 1.05rem; }}
        .menu-call {{ 
            padding: 18px 20px; border-top: 1px solid var(--border); 
            display: flex; align-items: center; gap: 12px;
            color: var(--primary); font-weight: 700; font-size: 1.1rem;
        }}
        .menu-call span {{ color: #e11d48; font-size: 1.3rem; }}

        /* Hero */
        .hero {{ background: var(--primary); color: var(--white); padding: 40px 0; overflow: hidden; }}
        .hero-grid {{ display: flex; flex-direction: column; gap: 30px; }}
        .hero-text {{ order: 1; }}
        .hero-img {{ order: 2; }}
        
        .hero-badge {{ 
            display: inline-block; background: rgba(183, 255, 60, 0.1); 
            color: var(--accent); padding: 6px 16px; border-radius: 50px;
            font-size: 0.85rem; font-weight: 600; border: 1px solid var(--accent); margin-bottom: 25px;
        }}
        .hero h1 {{ font-size: 2.2rem; margin-bottom: 15px; font-weight: 800; line-height: 1.1; color: var(--white); }}
        .hero-sub {{ font-size: 1.05rem; margin-bottom: 30px; opacity: 0.85; }}
        .hero-btns {{ display: flex; flex-direction: row; flex-wrap: wrap; gap: 12px; }}

        .hero-img img {{ border-radius: 12px; box-shadow: 0 20px 40px rgba(0,0,0,0.3); width: 100%; }}

        @media(min-width: 768px) {{
            body {{ padding-top: 64px; }}
            .navbar {{ height: 64px; }}
            .brand {{ font-size: 22px; }}
            .nav-menu {{ position: static; display: flex; flex-direction: row; width: auto; border: none; box-shadow: none; top: 0; align-items: center; }}
            .nav-menu a {{ padding: 0 15px; border: none; font-size: 0.95rem; }}
            .menu-call {{ border: none; padding: 0 15px; font-size: 1rem; }}
            .hamburger {{ display: none; }}
            
            .hero {{ padding: 100px 0; }}
            .hero-grid {{ flex-direction: row; gap: 60px; }}
            .hero-text {{ flex: 1.1; order: 1; }}
            .hero-img {{ flex: 0.9; order: 2; }}
            .hero h1 {{ font-size: 3.5rem; }}
            .hero-btns {{ flex-wrap: nowrap; }}
            .btn {{ flex: 0 1 auto; }}
        }}

        /* Trust Bar */
        .trust {{ padding: 30px 0; background: var(--white); border-bottom: 1px solid var(--border); }}
        .trust-grid {{ display: flex; flex-wrap: wrap; justify-content: center; gap: 12px; }}
        .chip {{ 
            background: var(--light); padding: 10px 18px; border-radius: 50px; font-weight: 600; font-size: 0.85rem;
            border: 1px solid var(--border); display: flex; align-items: center; gap: 8px;
        }}

        /* Services */
        .services {{ padding: 80px 0; }}
        .section-title {{ text-align: center; margin-bottom: 50px; font-size: 2.2rem; font-weight: 800; color: var(--primary); }}
        .services-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 24px; }}
        .card {{
            background: var(--white); padding: 30px; border-radius: 12px; box-shadow: var(--shadow);
            border: 1px solid var(--border); transition: transform 0.2s;
        }}
        .card:hover {{ transform: translateY(-5px); border-color: var(--accent); }}
        .card h3 {{ color: var(--primary); margin-bottom: 12px; display: flex; align-items: center; gap: 10px; }}
        .card-icon {{ font-size: 1.4rem; }}

        /* Reviews */
        .reviews {{ padding: 80px 0; background: #f3f4f6; text-align: center; }}
        .rating-line {{ font-weight: 700; font-size: 1.2rem; margin-bottom: 40px; color: var(--primary); }}
        .review-grid {{ display: grid; gap: 24px; max-width: 900px; margin: 0 auto; }}
        .review-card {{ background: var(--white); padding: 30px; border-radius: 12px; box-shadow: var(--shadow); text-align: left; }}
        .stars {{ color: #fbbf24; font-size: 1.2rem; margin-bottom: 10px; display: block; }}
        .review-author {{ font-weight: 700; margin-top: 20px; color: var(--primary); font-size: 0.9rem; }}

        /* Map */
        .map-section {{ padding: 80px 0; background: var(--white); }}
        .map-text {{ text-align: center; font-size: 1.1rem; color: #666; margin-bottom: 30px; }}
        .map-container {{ border-radius: 12px; overflow: hidden; box-shadow: var(--shadow); height: 400px; }}
        iframe {{ width: 100%; height: 100%; border: none; }}

        /* FAQ */
        .faq {{ padding: 80px 0; }}
        .accordion {{ max-width: 800px; margin: 0 auto; }}
        .accordion-item {{ border-bottom: 1px solid var(--border); }}
        .accordion-title {{ 
            padding: 20px 0; font-weight: 700; cursor: pointer; display: flex; justify-content: space-between; 
            color: var(--primary); font-size: 1.1rem;
        }}
        .accordion-content {{ padding-bottom: 20px; display: none; color: #555; }}
        .accordion-item.active .accordion-content {{ display: block; }}

        /* Form */
        .contact {{ padding: 80px 0; background: var(--primary); color: var(--white); }}
        .form-box {{ 
            background: var(--white); color: var(--text); padding: 40px; border-radius: 16px; 
            max-width: 600px; margin: 0 auto; box-shadow: 0 20px 50px rgba(0,0,0,0.3);
        }}
        .form-group {{ margin-bottom: 20px; }}
        .form-group label {{ display: block; margin-bottom: 8px; font-weight: 700; font-size: 0.9rem; }}
        .form-group input, .form-group select, .form-group textarea {{ 
            width: 100%; padding: 14px; border: 1px solid var(--border); border-radius: 8px; font-size: 1rem;
        }}
        .form-group textarea {{ height: 100px; resize: none; }}
        .success-msg {{ 
            display: none; background: #ecfdf5; color: #065f46; padding: 15px; border-radius: 8px; 
            text-align: center; margin-top: 20px; font-weight: 700; border: 1px solid #a7f3d0;
        }}
        .form-footer {{ margin-top: 25px; text-align: center; padding-top: 20px; border-top: 1px solid var(--border); }}
        .highlight {{ color: var(--primary); font-weight: 800; text-decoration: underline; }}

        /* Footer */
        footer {{ background: #07261d; color: #9ca3af; padding: 60px 0 20px; }}
        .footer-grid {{ display: grid; gap: 40px; }}
        .footer-brand {{ color: var(--white); font-size: 1.5rem; font-weight: 800; margin-bottom: 15px; }}
        .footer-col h4 {{ color: var(--white); margin-bottom: 20px; }}
        .footer-bottom {{ 
            margin-top: 60px; padding-top: 20px; border-top: 1px solid rgba(255,255,255,0.05); text-align: center; font-size: 0.8rem;
        }}

        @media(min-width: 768px) {{
            .footer-grid {{ grid-template-columns: 1fr 1fr; }}
        }}
    </style>
</head>
<body>

    <!-- NAVBAR -->
    <nav class="navbar">
        <div class="nav-container container">
            <a href="#" class="brand">{business_name}</a>
            <button class="hamburger" id="menuBtn">☰</button>
            <div class="nav-menu" id="navMenu">
                <a href="#services">Services</a>
                <a href="#reviews">Reviews</a>
                <a href="#map">Service Areas</a>
                <a href="#faq">FAQ</a>
                <a href="#quote">Get Free Quote</a>
                <a href="tel:{phone_clean}" class="menu-call">
                    <span>📞</span> Call {phone}
                </a>
            </div>
        </div>
    </nav>

    <!-- HERO -->
    <section class="hero">
        <div class="container hero-grid">
            <div class="hero-text">
                <div class="hero-badge">Plumbing Services in {location}</div>
                <h1>Professional Plumbing Services<br>in {location}</h1>
                <p class="hero-sub">Licensed, insured, and ready to help. Get top-rated local plumbing service today with same-day availability.</p>
                
                <div class="hero-btns">
                    <a href="tel:{phone_clean}" class="btn btn-primary">Call Now</a>
                    <a href="#quote" class="btn btn-outline">Get Free Quote</a>
                </div>
            </div>
            <div class="hero-img">
                <img src="assets/hero.webp" alt="Plumber in {location}" width="600" height="400" loading="eager" onerror="this.onerror=null; this.parentElement.style.background='rgba(255,255,255,0.1)';">
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
                <div class="chip">🤝 Warranty Included</div>
            </div>
        </div>
    </section>

    <!-- SERVICES -->
    <section class="services" id="services">
        <div class="container">
            <h2 class="section-title">Our Services</h2>
            <div class="services-grid">
                <div class="card">
                    <h3><span class="card-icon">🧹</span> Drain Cleaning</h3>
                    <p>Clear clogs and debris efficiently to keep your pipes flowing smoothly.</p>
                </div>
                <div class="card">
                    <h3><span class="card-icon">💧</span> Leak Repair</h3>
                    <p>Professional detection and repair for slab leaks, pipe bursts, and more.</p>
                </div>
                <div class="card">
                    <h3><span class="card-icon">🔥</span> Water Heater Service</h3>
                    <p>Installation, maintenance, and repair for tank and tankless water heaters.</p>
                </div>
                <div class="card">
                    <h3><span class="card-icon">🚽</span> Toilet Repair</h3>
                    <p>Fast fixes for running toilets, clogs, and new installations.</p>
                </div>
                <div class="card">
                    <h3><span class="card-icon">🔧</span> Sewer Line</h3>
                    <p>Advanced camera inspections and sewer line cleaning or replacement.</p>
                </div>
                <div class="card">
                    <h3><span class="card-icon">🚨</span> Emergency Plumbing</h3>
                    <p>24/7 availability for urgent plumbing crises when you need us most.</p>
                </div>
            </div>
        </div>
    </section>

    <!-- REVIEWS -->
    <section class="reviews" id="reviews">
        <div class="container">
            <h2 class="section-title">What Neighbors Say</h2>
            <div class="rating-line">4.9★ from 50+ Google Reviews</div>
            <div class="review-grid">
                <div class="review-card">
                    <span class="stars">★★★★★</span>
                    <p>"{business_name} saved the day! They arrived within an hour and fixed our leak immediately. Professional and clean!"</p>
                    <p class="review-author">- Chris, {city}</p>
                </div>
                <div class="review-card">
                    <span class="stars">★★★★★</span>
                    <p>"Professional, clean, and upfront about the cost. No surprises. Will definitely use them again for all my plumbing needs."</p>
                    <p class="review-author">- Taylor, {city}</p>
                </div>
            </div>
        </div>
    </section>

    <!-- MAP -->
    <section class="map-section" id="map">
        <div class="container">
            <h2 class="section-title">Serving {location}</h2>
            <p class="map-text">Serving {city} & surrounding areas with 5-star professional plumbing.</p>
            <div class="map-container">
                <iframe src="https://www.google.com/maps?q=Plumber+{url_location}&output=embed" allowfullscreen loading="lazy"></iframe>
            </div>
        </div>
    </section>

    <!-- FAQ -->
    <section class="faq" id="faq">
        <div class="container">
            <h2 class="section-title">Frequently Asked Questions</h2>
            <div class="accordion">
                <div class="accordion-item">
                    <div class="accordion-title">Do you offer same-day service? <span class="icon">+</span></div>
                    <div class="accordion-content">Yes, we strive to offer same-day service for most calls, especially emergencies.</div>
                </div>
                <div class="accordion-item">
                    <div class="accordion-title">Are you licensed and insured? <span class="icon">+</span></div>
                    <div class="accordion-content">Absolutely. We are fully licensed and insured for your protection and peace of mind.</div>
                </div>
            </div>
        </div>
    </section>

    <!-- FORM -->
    <section class="contact" id="quote">
        <div class="container">
            <h2 class="section-title">Get a Free Quote</h2>
            <div class="form-box">
                <form id="quoteForm" onsubmit="event.preventDefault(); document.getElementById('successMsg').style.display='block'; this.style.opacity='0.5';">
                    <div class="form-group">
                        <label>Name</label>
                        <input type="text" id="name" required placeholder="Your Name">
                    </div>
                    <div class="form-group">
                        <label>Phone</label>
                        <input type="tel" id="phone" required placeholder="Your Phone Number">
                    </div>
                    <button type="submit" class="btn btn-primary btn-full">Request Quote</button>
                    <div class="success-msg" id="successMsg">Thanks! We’ll call you back within 10 minutes.</div>
                </form>
                <div class="form-footer">
                    <p>Prefer to call? <a href="tel:{phone_clean}" class="highlight">{phone}</a></p>
                </div>
            </div>
        </div>
    </section>

    <!-- FOOTER -->
    <footer>
        <div class="container">
            <div class="footer-grid">
                <div class="footer-col">
                    <h4 class="footer-brand">{business_name}</h4>
                    <p>Professional plumbing services in {location}. Reliable, fast, and local.</p>
                </div>
                <div class="footer-col">
                    <h4>Contact Info</h4>
                    <p><strong>Phone:</strong> <a href="tel:{phone_clean}">{phone}</a></p>
                    <p><strong>Location:</strong> {location}</p>
                    <p><strong>Hours:</strong> Open 24 Hours</p>
                </div>
            </div>
            <div class="footer-bottom">
                <p>&copy; 2026 {business_name}. For emergencies, call immediately.</p>
            </div>
        </div>
    </footer>

    <script>
        // Navbar Scroll Effect
        window.addEventListener('scroll', () => {{
            const navbar = document.querySelector('.navbar');
            if (window.scrollY > 50) {{
                navbar.classList.add('scrolled');
            }} else {{
                navbar.classList.remove('scrolled');
            }}
        }});

        // Mobile Menu Toggle
        const menuBtn = document.getElementById('menuBtn');
        const navMenu = document.getElementById('navMenu');

        menuBtn.addEventListener('click', () => {{
            navMenu.classList.toggle('active');
            menuBtn.innerText = navMenu.classList.contains('active') ? '✕' : '☰';
        }});

        // FAQ Accordion
        document.querySelectorAll('.accordion-title').forEach(item => {{
            item.addEventListener('click', () => {{
                const parent = item.parentElement;
                parent.classList.toggle('active');
            }});
        }});
    </script>
</body>
</html>"""

# -----------------------------------------------------------------------------
# 2. OTHER TEMPLATES
# -----------------------------------------------------------------------------
# (Optional: Update Directory Template to say "Houston - Batch 2" etc.)
DIRECTORY_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Houston Plumbing Sites Directory</title>
    <style>
        body {{ font-family: system-ui, -apple-system, sans-serif; max-width: 900px; margin: 40px auto; padding: 0 20px; background: #f3f4f6; color: #374151; }}
        header {{ text-align: center; margin-bottom: 50px; }}
        h1 {{ color: #0b3d2e; font-size: 2.5rem; margin-bottom: 10px; }}
        .badge {{ display: inline-block; background: #0b3d2e; color: #fff; padding: 4px 12px; border-radius: 50px; font-size: 0.8rem; font-weight: 700; }}
        input {{ width: 100%; padding: 18px; font-size: 1.1rem; margin-bottom: 30px; border: 2px solid #e5e7eb; border-radius: 12px; box-sizing:border-box; box-shadow: 0 4px 6px -1px rgba(0,0,0,0.05); outline: none; transition: border-color 0.2s; }}
        input:focus {{ border-color: #0b3d2e; }}
        .list {{ display: grid; gap: 20px; }}
        .item {{ background: #fff; padding: 25px; border-radius: 12px; text-decoration: none; color: inherit; display: flex; justify-content: space-between; align-items: center; box-shadow: 0 1px 3px rgba(0,0,0,0.1); transition: all 0.2s; border: 1px solid transparent; }}
        .item:hover {{ transform: scale(1.02); box-shadow: 0 10px 15px -3px rgba(0,0,0,0.1); border-color: #b7ff3c; }}
        .item-info h3 {{ margin: 0 0 5px; color: #0b3d2e; font-size: 1.3rem; }}
        .item-info p {{ margin: 0; color: #6b7280; font-size: 0.95rem; }}
    </style>
</head>
<body>
    <header>
        <div class="badge">HOUSTON - BATCH 2</div>
        <h1>Plumbing Landing Pages</h1>
        <p>Metroflow-Aligned High-Converting Sites</p>
    </header>
    <input type="text" id="search" placeholder="Search by business name or location..." onkeyup="filter()">
    <div class="list" id="list">
        {links}
    </div>
    <script>
        function filter() {{
            const q = document.getElementById('search').value.toLowerCase();
            document.querySelectorAll('.item').forEach(el => {{
                el.style.display = el.innerText.toLowerCase().includes(q) ? 'flex' : 'none';
            }});
        }}
    </script>
</body>
</html>"""

# -----------------------------------------------------------------------------
# MAIN RUN
# -----------------------------------------------------------------------------
def run():
    if not os.path.exists(BRIEFS_DIR):
        os.makedirs(BRIEFS_DIR, exist_ok=True)

    generated_sites = []

    try:
        with open(CSV_PATH, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                slug = row['slug'].strip()
                biz_name = row['business_name'].strip()
                loc = row['location'].strip()
                phone = row['phone'].strip()
                
                # Directories
                site_path = os.path.join(SITES_DIR, slug)
                assets_path = os.path.join(site_path, 'assets')
                if not os.path.exists(assets_path):
                    os.makedirs(assets_path, exist_ok=True)
                
                if os.path.exists(SOURCE_ASSETS):
                    for item in os.listdir(SOURCE_ASSETS):
                        s = os.path.join(SOURCE_ASSETS, item)
                        d = os.path.join(assets_path, item)
                        if os.path.isfile(s):
                            shutil.copy2(s, d)

                # Generate File
                city, state = loc.split(',')[0].strip(), "TX"
                phone_clean = phone.replace(' ', '').replace('-', '').replace('(', '').replace(')', '').replace('+', '')
                url_location = loc.replace(' ', '+') 
                
                html_out = HTML_TEMPLATE.format(
                    business_name=biz_name,
                    location=loc,
                    phone=phone,
                    phone_clean=phone_clean,
                    city=city,
                    state=state,
                    url_location=url_location
                )
                
                with open(os.path.join(site_path, 'index.html'), 'w', encoding='utf-8') as hf:
                    hf.write(html_out)
                
                print(f"Generated site: {slug}")
                generated_sites.append({"name": biz_name, "slug": slug, "loc": loc})

        # Directory Page
        links_html = ""
        for s in generated_sites:
            links_html += f'''<a href="{s["slug"]}/index.html" class="item"><div class="item-info"><h3>{s["name"]}</h3><p>{s["loc"]}</p></div><div class="item-arrow">→</div></a>'''
        
        with open(os.path.join(SITES_DIR, 'index.html'), 'w', encoding='utf-8') as df:
            df.write(DIRECTORY_TEMPLATE.format(links=links_html))
            
        print(f"Generated directory page with {len(generated_sites)} sites.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    run()
