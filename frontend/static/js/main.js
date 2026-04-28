/* =============================================================
   🎉 Party Magic - Main JavaScript
   إدارة الأنيميشن، التفاعلات، والتنقل
   ============================================================= */

// ============ Page Loader ============
window.addEventListener('load', () => {
    setTimeout(() => {
        const loader = document.getElementById('page-loader');
        if (loader) loader.classList.add('hidden');
    }, 500);
});

// ============ AOS Init ============
document.addEventListener('DOMContentLoaded', () => {
    if (typeof AOS !== 'undefined') {
        AOS.init({
            duration: 800,
            easing: 'ease-out-cubic',
            once: true,
            offset: 80,
            mirror: false,
        });
    }
});

// ============ Navigation Scroll Effect ============
const nav = document.getElementById('main-nav');
let lastScroll = 0;

window.addEventListener('scroll', () => {
    const currentScroll = window.pageYOffset;
    if (nav) {
        if (currentScroll > 50) {
            nav.classList.add('scrolled');
        } else {
            nav.classList.remove('scrolled');
        }
    }
    lastScroll = currentScroll;
});

// ============ Mobile Menu ============
const mobileMenuBtn = document.getElementById('mobile-menu-btn');
const mobileMenu = document.getElementById('mobile-menu');
const mobileClose = document.getElementById('mobile-close');

if (mobileMenuBtn && mobileMenu) {
    mobileMenuBtn.addEventListener('click', () => {
        mobileMenu.classList.remove('translate-x-full');
        document.body.style.overflow = 'hidden';
    });
}
if (mobileClose) {
    mobileClose.addEventListener('click', () => {
        mobileMenu.classList.add('translate-x-full');
        document.body.style.overflow = '';
    });
}
// إغلاق القائمة عند النقر على رابط
document.querySelectorAll('#mobile-menu a').forEach(link => {
    link.addEventListener('click', () => {
        mobileMenu.classList.add('translate-x-full');
        document.body.style.overflow = '';
    });
});

// ============ Counter Animation ============
function animateCounter(el, target, duration = 2000) {
    const start = 0;
    const startTime = performance.now();
    const suffix = el.dataset.suffix || '';

    function update(now) {
        const elapsed = now - startTime;
        const progress = Math.min(elapsed / duration, 1);
        const eased = 1 - Math.pow(1 - progress, 3); // ease-out cubic
        const current = Math.floor(start + (target - start) * eased);
        el.textContent = current.toLocaleString('ar-EG') + suffix;
        if (progress < 1) requestAnimationFrame(update);
        else el.textContent = target.toLocaleString('ar-EG') + suffix;
    }
    requestAnimationFrame(update);
}

const counterObserver = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
        if (entry.isIntersecting) {
            const el = entry.target;
            if (!el.dataset.animated) {
                el.dataset.animated = 'true';
                const target = parseInt(el.dataset.target || el.textContent.replace(/[^\d]/g, ''));
                animateCounter(el, target);
            }
        }
    });
}, { threshold: 0.5 });

document.querySelectorAll('[data-counter]').forEach(el => counterObserver.observe(el));

// ============ Confetti Function ============
function fireConfetti(options = {}) {
    if (typeof confetti === 'undefined') return;
    const defaults = {
        particleCount: 100,
        spread: 80,
        origin: { y: 0.6 },
        colors: ['#FF6B6B', '#4ECDC4', '#FFE66D', '#A855F7', '#FF8FB1'],
    };
    confetti({ ...defaults, ...options });
}

function celebrationConfetti() {
    if (typeof confetti === 'undefined') return;
    const duration = 2500;
    const animationEnd = Date.now() + duration;
    const colors = ['#FF6B6B', '#4ECDC4', '#FFE66D', '#A855F7'];

    (function frame() {
        confetti({ particleCount: 4, angle: 60, spread: 55, origin: { x: 0 }, colors });
        confetti({ particleCount: 4, angle: 120, spread: 55, origin: { x: 1 }, colors });
        if (Date.now() < animationEnd) requestAnimationFrame(frame);
    }());
}

// ============ Hero GSAP Animations ============
if (typeof gsap !== 'undefined') {
    // Helper: only animate if elements exist on current page
    const animateIfExists = (selector, props) => {
        if (document.querySelector(selector)) {
            return gsap.from(selector, props);
        }
        return null;
    };

    // Hero entrance animation - only runs on pages with hero structure
    if (document.querySelector('.hero-image-frame') || document.querySelector('.hero-title-line')) {
        const heroTl = gsap.timeline({ delay: 0.3 });
        if (document.querySelector('.hero-badge')) heroTl.from('.hero-badge', { opacity: 0, y: -30, duration: 0.6, ease: 'back.out(1.7)' });
        if (document.querySelector('.hero-title-line')) heroTl.from('.hero-title-line', { opacity: 0, y: 50, duration: 0.8, stagger: 0.15, ease: 'power3.out' }, '-=0.3');
        if (document.querySelector('.hero-description')) heroTl.from('.hero-description', { opacity: 0, y: 30, duration: 0.7 }, '-=0.4');
        if (document.querySelector('.hero-cta')) heroTl.from('.hero-cta', { opacity: 0, y: 30, duration: 0.6, stagger: 0.15 }, '-=0.4');
        if (document.querySelector('.hero-stats-mini > *')) heroTl.from('.hero-stats-mini > *', { opacity: 0, y: 20, duration: 0.5, stagger: 0.1 }, '-=0.3');
        if (document.querySelector('.hero-image-frame')) heroTl.from('.hero-image-frame', { opacity: 0, scale: 0.7, rotation: -10, duration: 1, ease: 'back.out(1.4)' }, '-=1.2');
    }

    // Floating mascots (works on every page)
    gsap.utils.toArray('.hero-mascot').forEach((m, i) => {
        gsap.to(m, {
            y: -20,
            rotation: i % 2 === 0 ? 5 : -5,
            duration: 2 + Math.random() * 2,
            repeat: -1,
            yoyo: true,
            ease: 'sine.inOut',
            delay: i * 0.2,
        });
    });

    // Scroll-triggered reveals (fallback if AOS missing)
    if (typeof ScrollTrigger !== 'undefined') {
        gsap.registerPlugin(ScrollTrigger);
    }
}

// ============ Gallery Filter ============
function initGalleryFilter() {
    const filterBtns = document.querySelectorAll('.gallery-filter-btn');
    const items = document.querySelectorAll('.gallery-item');
    if (!filterBtns.length || !items.length) return;

    filterBtns.forEach(btn => {
        btn.addEventListener('click', () => {
            const filter = btn.dataset.filter;
            filterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');

            items.forEach(item => {
                const matches = filter === 'all' || item.dataset.category === filter;
                if (matches) {
                    item.style.display = '';
                    setTimeout(() => {
                        item.style.opacity = '1';
                        item.style.transform = 'scale(1)';
                    }, 50);
                } else {
                    item.style.opacity = '0';
                    item.style.transform = 'scale(0.8)';
                    setTimeout(() => { item.style.display = 'none'; }, 300);
                }
            });
        });
    });
}

// ============ Lightbox ============
function initLightbox() {
    const items = document.querySelectorAll('.gallery-item');
    let lightbox = document.getElementById('lightbox');
    if (!lightbox) {
        lightbox = document.createElement('div');
        lightbox.id = 'lightbox';
        lightbox.className = 'lightbox';
        lightbox.innerHTML = `
            <div class="lightbox-close"><i class="fas fa-times"></i></div>
            <img src="" alt="">
        `;
        document.body.appendChild(lightbox);
    }
    const lightboxImg = lightbox.querySelector('img');
    const lightboxClose = lightbox.querySelector('.lightbox-close');

    items.forEach(item => {
        item.addEventListener('click', () => {
            const img = item.querySelector('img');
            if (img) {
                lightboxImg.src = img.src;
                lightboxImg.alt = img.alt;
                lightbox.classList.add('active');
                document.body.style.overflow = 'hidden';
            }
        });
    });

    const closeLightbox = () => {
        lightbox.classList.remove('active');
        document.body.style.overflow = '';
    };
    lightboxClose.addEventListener('click', closeLightbox);
    lightbox.addEventListener('click', (e) => { if (e.target === lightbox) closeLightbox(); });
    document.addEventListener('keydown', (e) => { if (e.key === 'Escape') closeLightbox(); });
}

// ============ Contact Form ============
async function handleContactForm(e) {
    e.preventDefault();
    const form = e.target;
    const btn = form.querySelector('button[type="submit"]');
    const originalText = btn.innerHTML;
    btn.disabled = true;
    btn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> جاري الإرسال...';

    const data = {
        name: form.name.value,
        phone: form.phone.value,
        email: form.email.value,
        subject: form.subject?.value || '',
        message: form.message.value,
    };

    try {
        const res = await fetch('/api/contact', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(data),
        });
        if (!res.ok) throw new Error('فشل الإرسال');
        showToast('🎉 تم إرسال رسالتك بنجاح! سنتواصل معك قريباً', 'success');
        fireConfetti();
        form.reset();
    } catch (err) {
        showToast('❌ حدث خطأ، حاول مرة أخرى', 'error');
    } finally {
        btn.disabled = false;
        btn.innerHTML = originalText;
    }
}

// ============ Toast Notifications ============
function showToast(message, type = 'info') {
    let container = document.getElementById('toast-container');
    if (!container) {
        container = document.createElement('div');
        container.id = 'toast-container';
        container.className = 'fixed top-24 left-1/2 -translate-x-1/2 z-[10000] flex flex-col gap-2 pointer-events-none';
        document.body.appendChild(container);
    }
    const toast = document.createElement('div');
    const colors = {
        success: 'bg-gradient-to-r from-emerald-500 to-teal-500',
        error: 'bg-gradient-to-r from-rose-500 to-red-500',
        info: 'bg-gradient-to-r from-primary to-magic',
    };
    toast.className = `${colors[type]} text-white px-6 py-3 rounded-2xl shadow-2xl pointer-events-auto transform translate-y-[-20px] opacity-0 transition-all duration-500 max-w-md text-center font-bold`;
    toast.textContent = message;
    container.appendChild(toast);
    requestAnimationFrame(() => {
        toast.style.transform = 'translateY(0)';
        toast.style.opacity = '1';
    });
    setTimeout(() => {
        toast.style.transform = 'translateY(-20px)';
        toast.style.opacity = '0';
        setTimeout(() => toast.remove(), 500);
    }, 4000);
}

// Expose globally
window.showToast = showToast;
window.fireConfetti = fireConfetti;
window.celebrationConfetti = celebrationConfetti;

// Init page-specific code
document.addEventListener('DOMContentLoaded', () => {
    initGalleryFilter();
    initLightbox();
    const contactForm = document.getElementById('contact-form');
    if (contactForm) contactForm.addEventListener('submit', handleContactForm);
});
