
const translations = {
    en: {
        home: "Home",
        services: "Services",
        doctors: "Doctors",
        reviews: "Reviews",
        contact: "Contact",
        heroHeadline: "Premium Dental Care in Al Muteena - Deira",
        heroSub: "Experience world-class dentistry with a gentle touch. DHA-certified experts dedicated to your perfect smile.",
        bookBtn: "Book Appointment",
        callBtn: "Call Now",
        whatsappBtn: "WhatsApp Us",
        trustLine: "✓ DHA-certified doctors · ✓ Arabic-speaking staff · ✓ Same-week appointments",
        servicesTitle: "Comprehensive Dental Services",
        servicesSub: "Advanced treatments for the whole family.",
        serv1: "General Dentistry",
        serv1desc: "Routine checkups, cleaning, and fillings.",
        serv2: "Invisalign & Braces",
        serv2desc: "Straighten your teeth discreetly.",
        serv3: "Hollywood Smile",
        serv3desc: "Veneers and whitening for a celebrity look.",
        serv4: "Dental Implants",
        serv4desc: "Permanent solutions for missing teeth.",
        serv5: "Pediatric Dentistry",
        serv5desc: "Gentle care for your little ones.",
        moreDetails: "WhatsApp for details",
        baTitle: "Real Patient Results",
        baSub: "See the difference we make.",
        baCaption: "Veneers + whitening results",
        baDisclaimer: "Results vary by patient.",
        docTitle: "Meet Our Experts",
        docSub: "Highly qualified professionals you can trust.",
        docExp: "Experience",
        docLang: "Languages",
        reviewsTitle: "What Our Patients Say",
        formTitle: "Request a Callback",
        formName: "Your Name",
        formPhone: "Phone Number",
        formTreat: "Treatment Needed",
        formMsg: "Message (Optional)",
        formSubmit: "Request Callback",
        locTitle: "Visit Us",
        footerDesc: "Your trusted partners in oral health.",
        quickLinks: "Quick Links",
        hours: "Working Hours",
        rights: "All rights reserved."
    },
    ar: {
        home: "الرئيسية",
        services: "خدماتنا",
        doctors: "أطباؤنا",
        reviews: "آراء المرضى",
        contact: "اتصل بنا",
        heroHeadline: "رعاية أسنان متميزة في بر دبي",
        heroSub: "استمتع بطب أسنان عالمي المستوى بلمسة لطيفة. خبراء معتمدون من هيئة الصحة بدبي مكرسون لابتسامتك المثالية.",
        bookBtn: "حجز موعد",
        callBtn: "اتصل الآن",
        whatsappBtn: "واتساب",
        trustLine: "✓ أطباء معتمدون · ✓ طاقم يتحدث العربية · ✓ مواعيد في نفس الأسبوع",
        servicesTitle: "خدمات أسنان شاملة",
        servicesSub: "علاجات متقدمة لجميع أفراد الأسرة.",
        serv1: "طب الأسنان العام",
        serv1desc: "فحوصات دورية، تنظيف، وحشوات.",
        serv2: "تقويم الأسنان و إنفزلاين",
        serv2desc: "قوم أسنانك بشكل غير مرئي.",
        serv3: "ابتسامة هوليود",
        serv3desc: "عدسات وتبييض لمظهر المشاهير.",
        serv4: "زراعة الأسنان",
        serv4desc: "حلول دائمة للأسنان المفقودة.",
        serv5: "طب أسنان الأطفال",
        serv5desc: "رعاية لطيفة لأطفالك.",
        moreDetails: "تواصل عبر واتساب للتفاصيل",
        baTitle: "نتائج حقيقية للمرضى",
        baSub: "شاهد الفرق الذي نصنعه.",
        baCaption: "نتائج العدسات + التبييض",
        baDisclaimer: "تختلف النتائج من مريض لآخر.",
        docTitle: "تعرف على خبرائنا",
        docSub: "مهنيون مؤهلون تأهيلا عاليا يمكنك الوثوق بهم.",
        docExp: "الخبرة",
        docLang: "اللغات",
        reviewsTitle: "ماذا يقول مرضانا",
        formTitle: "اطلب معاودة الاتصال",
        formName: "الاسم",
        formPhone: "رقم الهاتف",
        formTreat: "العلاج المطلوب",
        formMsg: "رسالة (اختياري)",
        formSubmit: "اطلب الاتصال",
        locTitle: "زورونا",
        footerDesc: "شركاؤك الموثوقون في صحة الفم.",
        quickLinks: "روابط سريعة",
        hours: "ساعات العمل",
        rights: "جميع الحقوق محفوظة."
    }
};

document.addEventListener('DOMContentLoaded', () => {
    // Mobile Menu
    const menuBtn = document.getElementById('menuBtn');
    const mobileMenu = document.getElementById('mobileMenu');

    if (menuBtn) {
        menuBtn.addEventListener('click', () => {
            mobileMenu.classList.toggle('active');
            menuBtn.textContent = mobileMenu.classList.contains('active') ? '✕' : '☰';
        });
    }

    // Dynamic Year
    const yearEl = document.getElementById('year');
    if (yearEl) yearEl.textContent = new Date().getFullYear();

    // Language Toggle logic for multiple buttons (desktop + mobile)
    const langToggleBtns = document.querySelectorAll('.lang-toggle');

    // Check local storage
    let currentLang = localStorage.getItem('lang') || 'en';
    applyLanguage(currentLang);

    langToggleBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            currentLang = currentLang === 'en' ? 'ar' : 'en';
            localStorage.setItem('lang', currentLang);
            applyLanguage(currentLang);
        });
    });

    // Contact Form Logic (No WhatsApp Redirect)
    const contactForm = document.getElementById('contactForm');
    if (contactForm) {
        contactForm.addEventListener('submit', (e) => {
            e.preventDefault();

            const btn = contactForm.querySelector('button[type="submit"]');
            // Store original text
            if (!btn.hasAttribute('data-original-text')) {
                btn.setAttribute('data-original-text', btn.textContent);
            }
            const originalText = btn.getAttribute('data-original-text');

            // Loading State
            btn.textContent = currentLang === 'en' ? 'Sending...' : 'جاري الإرسال...';
            btn.disabled = true;

            // Simulate Success
            setTimeout(() => {
                btn.textContent = currentLang === 'en' ?
                    'Thank you! We will contact you shortly.' :
                    'شكراً لك! سنتواصل معك قريباً.';

                btn.style.backgroundColor = '#10b981'; // Green
                btn.style.borderColor = '#10b981';
                contactForm.reset();

                // Reset after 5 seconds
                setTimeout(() => {
                    const key = btn.getAttribute('data-i18n');
                    if (key && translations[currentLang][key]) {
                        btn.textContent = translations[currentLang][key];
                    } else {
                        btn.textContent = originalText;
                    }
                    btn.disabled = false;
                    btn.style.backgroundColor = '';
                    btn.style.borderColor = '';
                }, 5000);
            }, 1500);
        });
    }
});

function applyLanguage(lang) {
    const html = document.documentElement;
    html.setAttribute('dir', lang === 'ar' ? 'rtl' : 'ltr');
    html.setAttribute('lang', lang);

    // Update All Toggle Buttons Text
    const langTexts = document.querySelectorAll('.currentLangText');
    langTexts.forEach(span => {
        span.textContent = lang === 'en' ? 'العربية' : 'English';
    });

    // Update Text Content
    const dataEls = document.querySelectorAll('[data-i18n]');
    dataEls.forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (translations[lang][key]) {
            el.textContent = translations[lang][key];
        }
    });

    // Special handling for input placeholders if needed
    const inputs = document.querySelectorAll('[data-i18n-placeholder]');
    inputs.forEach(el => {
        const key = el.getAttribute('data-i18n-placeholder');
        if (translations[lang][key]) {
            el.placeholder = translations[lang][key];
        }
    });
}
