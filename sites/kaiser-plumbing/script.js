// Navbar Scroll Effect
window.addEventListener('scroll', () => {
    const navbar = document.querySelector('.navbar');
    if (window.scrollY > 50) {
        navbar.classList.add('scrolled');
    } else {
        navbar.classList.remove('scrolled');
    }
});

// Mobile Menu Toggle
const menuBtn = document.getElementById('menuBtn');
const navMenu = document.getElementById('navMenu');

menuBtn.addEventListener('click', () => {
    navMenu.classList.toggle('active');
    menuBtn.innerText = navMenu.classList.contains('active') ? '✕' : '☰';
});

// Close menu when clicking links
document.querySelectorAll('.nav-menu a').forEach(link => {
    link.addEventListener('click', () => {
        navMenu.classList.remove('active');
        menuBtn.innerText = '☰';
    });
});

// FAQ Accordion
document.querySelectorAll('.accordion-title').forEach(item => {
    item.addEventListener('click', () => {
        const parent = item.parentElement;
        parent.classList.toggle('active');
        item.querySelector('.icon').innerText = parent.classList.contains('active') ? '−' : '+';
    });
});

// Form Submission
const quoteForm = document.getElementById('quoteForm');
const successMsg = document.getElementById('successMsg');

if (quoteForm) {
    quoteForm.addEventListener('submit', (e) => {
        e.preventDefault();
        
        // In a real app, you would send data to a backend here
        
        quoteForm.style.opacity = '0.5';
        quoteForm.style.pointerEvents = 'none';
        successMsg.style.display = 'block';
        
        // Optional: Reset form after delay
        setTimeout(() => {
            quoteForm.reset();
            quoteForm.style.opacity = '1';
            quoteForm.style.pointerEvents = 'auto';
            // successMsg.style.display = 'none';
        }, 3000);
    });
}
