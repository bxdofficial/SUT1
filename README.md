# 🎉 Party Magic - موقع شركة حفلات الماسكات

موقع إلكتروني احترافي ومتكامل لشركة تنظيم حفلات الأطفال والماسكات في مصر.

![Status](https://img.shields.io/badge/status-production_ready-brightgreen)
![Python](https://img.shields.io/badge/python-3.11+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110-009688)
![License](https://img.shields.io/badge/license-MIT-purple)

---

## ✨ المميزات

### 🎨 واجهة المستخدم
- **تصميم عصري وملوّن** مع نظام Glassmorphism احترافي
- **دعم كامل للعربية (RTL)** مع خطوط مُحسّنة (Cairo, Fredoka, Nunito)
- **أنيميشن متقدمة** باستخدام GSAP, AOS, Framer-style transitions
- **تأثيرات Confetti** عند نجاح الحجوزات
- **متجاوب تماماً** مع جميع أحجام الشاشات (Mobile-first)
- **شريط تنقل ذكي** يتأقلم مع التمرير
- **زر واتساب عائم** للتواصل السريع

### 📱 الصفحات
1. **الصفحة الرئيسية** - Hero section مذهل، إحصائيات متحركة، عرض الخدمات والشخصيات والشهادات
2. **الخدمات** - عرض كل الباقات + جدول مقارنة + إضافات اختيارية
3. **الشخصيات** - معرض الماسكات مع فلترة بالفئات
4. **المعرض** - Masonry gallery مع Lightbox وفلترة
5. **الحجز** - نموذج 5 خطوات (Wizard) مع حساب السعر المباشر
6. **التواصل** - نموذج تواصل + خريطة + FAQ
7. **لوحة الإدارة** - إدارة الحجوزات والرسائل + إحصائيات

### 🔧 التقنيات

#### الباك إند
- **FastAPI** - أحدث وأسرع إطار عمل Python
- **SQLAlchemy 2.0** - ORM متقدم
- **SQLite** (افتراضي) / **PostgreSQL** (للإنتاج)
- **Pydantic 2** - التحقق من البيانات
- **JWT + bcrypt** - مصادقة آمنة للأدمن
- **Jinja2** - قوالب الصفحات

#### الفرونت إند
- **Tailwind CSS** - تصميم سريع وحديث
- **GSAP 3** - أنيميشن احترافية
- **AOS** - Scroll animations
- **Swiper.js** - سلايدرات احترافية
- **Canvas Confetti** - تأثيرات احتفالية
- **Font Awesome** - أيقونات

---

## 🚀 التشغيل

### الطريقة الأولى: تشغيل محلي مباشر

```bash
# 1. تثبيت الاعتماديات
pip install -r requirements.txt

# 2. تشغيل الخادم
python -m uvicorn backend.main:app --host 0.0.0.0 --port 8000 --reload
```

سيتم فتح الموقع تلقائياً على: `http://localhost:8000`

### الطريقة الثانية: Docker

```bash
docker-compose up --build
```

---

## 🔐 لوحة الإدارة

- **الرابط:** `/admin`
- **اسم المستخدم:** `admin`
- **كلمة المرور:** `admin123`

⚠️ **مهم:** غيّر كلمة المرور في الإنتاج عبر تعديل `backend/seed_data.py` أو إضافة مستخدم جديد.

---

## 📁 هيكل المشروع

```
webapp/
├── backend/                    # تطبيق FastAPI
│   ├── __init__.py
│   ├── main.py                # نقطة الدخول الرئيسية - Routes & APIs
│   ├── database.py            # إعدادات قاعدة البيانات
│   ├── models.py              # نماذج SQLAlchemy
│   ├── schemas.py             # Pydantic schemas
│   └── seed_data.py           # البيانات الأولية (شخصيات، خدمات، إلخ)
│
├── frontend/
│   ├── templates/             # قوالب Jinja2
│   │   ├── base.html         # القالب الأساسي (header, footer, nav)
│   │   ├── index.html        # الصفحة الرئيسية
│   │   ├── services.html     # صفحة الخدمات
│   │   ├── characters.html   # صفحة الشخصيات
│   │   ├── gallery.html      # المعرض
│   │   ├── booking.html      # نموذج الحجز
│   │   ├── contact.html      # تواصل معنا
│   │   ├── admin_login.html  # تسجيل دخول الأدمن
│   │   └── admin_dashboard.html # لوحة التحكم
│   │
│   └── static/
│       ├── css/
│       │   └── style.css     # CSS مخصص (1700+ سطر)
│       ├── js/
│       │   └── main.js       # JavaScript تفاعلي
│       └── images/           # صور الموقع
│
├── uploads/                   # مجلد التحميلات
├── requirements.txt           # اعتماديات Python
├── Dockerfile                 # ملف Docker
├── docker-compose.yml        # تركيبة Docker Compose
├── party.db                   # قاعدة البيانات SQLite (تُنشأ تلقائياً)
└── README.md                  # هذا الملف
```

---

## 🌐 API Endpoints

### Public APIs
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | فحص صحة الخادم |
| GET | `/api/services` | قائمة الخدمات والباقات |
| GET | `/api/characters?category=...` | قائمة الشخصيات (مع فلترة) |
| GET | `/api/gallery?category=...` | عناصر المعرض |
| GET | `/api/testimonials` | شهادات العملاء |
| GET | `/api/stats` | إحصائيات عامة |
| POST | `/api/bookings` | إنشاء حجز جديد |
| GET | `/api/bookings/{code}` | التحقق من حجز |
| POST | `/api/contact` | إرسال رسالة تواصل |

### Admin APIs (تتطلب Cookie مصادقة)
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/api/admin/bookings/{id}/status` | تحديث حالة الحجز |

---

## 🎨 نظام الألوان

| الاسم | الكود | الاستخدام |
|------|------|---------|
| Primary | `#FF6B6B` | اللون الأساسي - أحمر مرجاني |
| Secondary | `#4ECDC4` | تركوازي - للنجاح والسلام |
| Accent | `#FFE66D` | أصفر ذهبي - للتمييز |
| Magic | `#A855F7` | بنفسجي - للسحر والمرح |
| Cream | `#FFF9F0` | خلفية فاتحة |
| Midnight | `#0D0D1A` | خلفية داكنة |

---

## 📊 قاعدة البيانات

الجداول الرئيسية:
- **services** - الخدمات والباقات
- **characters** - الشخصيات والماسكات
- **bookings** - الحجوزات
- **gallery** - صور المعرض
- **testimonials** - شهادات العملاء
- **users** - المستخدمين والأدمن
- **contact_messages** - رسائل التواصل

---

## 🔒 الأمان

- ✅ تشفير كلمات المرور بـ bcrypt
- ✅ HttpOnly cookies للمصادقة
- ✅ JWT tokens مع انتهاء صلاحية
- ✅ التحقق من صلاحيات الأدمن
- ✅ Pydantic validation لكل المدخلات
- ✅ SQL injection prevention عبر SQLAlchemy ORM

---

## 🌍 النشر للإنتاج

### 1. متغيرات البيئة (مهم!)
عند النشر، عدّل `SECRET_KEY` في `backend/main.py`:

```python
SECRET_KEY = os.environ.get("SECRET_KEY", "your-very-strong-secret-key")
```

### 2. استخدام PostgreSQL
في `backend/database.py`:
```python
SQLALCHEMY_DATABASE_URL = os.environ.get("DATABASE_URL", "postgresql://user:pass@host/db")
```

### 3. Tailwind للإنتاج
الموقع يستخدم Tailwind CDN حالياً. للإنتاج:
- ثبّت Tailwind CLI
- ابنِ ملف CSS مُجمّع

---

## 🎯 المميزات المستقبلية المخططة

- [ ] نظام دفع إلكتروني (فودافون كاش، إنستاباي)
- [ ] إشعارات WhatsApp تلقائية للحجوزات
- [ ] نظام تقويم تفاعلي للمواعيد
- [ ] رفع صور المعرض من لوحة الإدارة
- [ ] دعم متعدد اللغات (عربي/إنجليزي)
- [ ] تطبيق موبايل (PWA)
- [ ] نظام نقاط الولاء للعملاء

---

## 📞 الدعم والتواصل

للدعم الفني أو الاستفسارات حول المشروع:
- 📧 البريد: info@partymagic.eg
- 💬 واتساب: +20 100 123 4567

---

## 📜 الترخيص

MIT License - استخدمه بحرية لمشاريعك التجارية أو الشخصية.

---

**صُنع بـ ❤️ لإسعاد أطفالنا** 🎉
