"""
🎉 Party Magic - موقع شركة حفلات الماسكات الاحترافي 🎉
================================================================
التطبيق الرئيسي - FastAPI Backend + Server-Side Rendered Frontend

يحتوي على:
- API endpoints لإدارة الحجوزات والخدمات والشخصيات
- صفحات HTML مع قوالب Jinja2
- لوحة تحكم للأدمن
- خدمة الملفات الثابتة (CSS, JS, Images)
"""
import os
import random
import string
from datetime import datetime, timedelta
from typing import List, Optional

from fastapi import FastAPI, Depends, HTTPException, Request, Form, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
import bcrypt
from jose import jwt, JWTError

from .database import engine, Base, get_db
from . import models, schemas
from .seed_data import seed_database


# ============ إعدادات أساسية ============
SECRET_KEY = "party-magic-super-secret-key-change-in-production-2024"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOURS = 24

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATES_DIR = os.path.join(BASE_DIR, "frontend", "templates")
STATIC_DIR = os.path.join(BASE_DIR, "frontend", "static")
UPLOADS_DIR = os.path.join(BASE_DIR, "uploads")
os.makedirs(UPLOADS_DIR, exist_ok=True)

# تشفير كلمات المرور باستخدام bcrypt مباشرة (تجنبًا لتعارض إصدارات passlib)
def verify_password(plain: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(plain.encode("utf-8")[:72], hashed.encode("utf-8"))
    except Exception:
        return False

# إنشاء التطبيق
app = FastAPI(
    title="Party Magic API 🎉",
    description="موقع شركة تنظيم حفلات الأطفال والماسكات",
    version="1.0.0",
)

# CORS - السماح للـ frontend بالاتصال
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# إعداد Jinja2 templates
templates = Jinja2Templates(directory=TEMPLATES_DIR)

# تركيب الملفات الثابتة
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")
app.mount("/uploads", StaticFiles(directory=UPLOADS_DIR), name="uploads")


# ============ Events ============
@app.on_event("startup")
async def startup_event():
    """تشغيل عند بدء التطبيق - إنشاء الجداول وتعبئة البيانات الأولية"""
    Base.metadata.create_all(bind=engine)
    seed_database()
    print("🚀 تطبيق Party Magic جاهز للعمل!")


# ============ مساعدات ============
def generate_booking_code() -> str:
    """توليد كود حجز فريد PRTY-XXXXX"""
    return "PRTY-" + "".join(random.choices(string.ascii_uppercase + string.digits, k=6))


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    """إنشاء JWT access token"""
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(hours=ACCESS_TOKEN_EXPIRE_HOURS))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def verify_admin(request: Request, db: Session = Depends(get_db)) -> Optional[models.User]:
    """التحقق من صلاحيات الأدمن من الكوكي"""
    token = request.cookies.get("admin_token")
    if not token:
        return None
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username = payload.get("sub")
        if not username:
            return None
        user = db.query(models.User).filter(models.User.username == username).first()
        if user and user.is_admin:
            return user
    except JWTError:
        return None
    return None


def get_global_context(db: Session) -> dict:
    """بيانات مشتركة بين كل الصفحات"""
    return {
        "company_name": "Party Magic",
        "company_name_ar": "بارتي ماجيك",
        "phone": "+20 100 123 4567",
        "whatsapp": "201001234567",
        "email": "info@partymagic.eg",
        "address": "القاهرة، مصر",
        "year": datetime.now().year,
    }


# ============ صفحات HTML ============

@app.get("/", response_class=HTMLResponse)
async def home(request: Request, db: Session = Depends(get_db)):
    """الصفحة الرئيسية - Hero, Stats, Services Preview, Characters, Testimonials"""
    services = db.query(models.Service).filter(models.Service.is_active == True).order_by(models.Service.order, models.Service.id).limit(6).all()
    characters = db.query(models.Character).filter(models.Character.is_featured == True).limit(6).all()
    if not characters:
        characters = db.query(models.Character).limit(6).all()
    testimonials = db.query(models.Testimonial).filter(models.Testimonial.is_featured == True).limit(6).all()
    gallery_preview = db.query(models.GalleryItem).filter(models.GalleryItem.is_featured == True).limit(8).all()

    # إحصائيات
    total_bookings = db.query(models.Booking).count()
    total_characters = db.query(models.Character).count()

    stats = {
        "happy_clients": max(total_bookings + 247, 250),  # رقم مبدئي مضاف
        "parties_organized": max(total_bookings + 312, 320),
        "characters": total_characters,
        "years_experience": 8,
    }

    ctx = {
        "request": request,
        "services": services,
        "characters": characters,
        "testimonials": testimonials,
        "gallery_preview": gallery_preview,
        "stats": stats,
        "active_page": "home",
        **get_global_context(db),
    }
    return templates.TemplateResponse(request, "index.html", ctx)


@app.get("/services", response_class=HTMLResponse)
async def services_page(request: Request, db: Session = Depends(get_db)):
    """صفحة الخدمات والباقات"""
    services = db.query(models.Service).filter(models.Service.is_active == True).order_by(models.Service.price).all()
    ctx = {
        "request": request,
        "services": services,
        "active_page": "services",
        **get_global_context(db),
    }
    return templates.TemplateResponse(request, "services.html", ctx)


@app.get("/characters", response_class=HTMLResponse)
async def characters_page(request: Request, db: Session = Depends(get_db)):
    """صفحة الشخصيات والماسكات"""
    characters = db.query(models.Character).filter(models.Character.is_available == True).all()
    ctx = {
        "request": request,
        "characters": characters,
        "active_page": "characters",
        **get_global_context(db),
    }
    return templates.TemplateResponse(request, "characters.html", ctx)


@app.get("/gallery", response_class=HTMLResponse)
async def gallery_page(request: Request, db: Session = Depends(get_db)):
    """صفحة المعرض"""
    gallery = db.query(models.GalleryItem).order_by(desc(models.GalleryItem.created_at)).all()
    ctx = {
        "request": request,
        "gallery": gallery,
        "active_page": "gallery",
        **get_global_context(db),
    }
    return templates.TemplateResponse(request, "gallery.html", ctx)


@app.get("/booking", response_class=HTMLResponse)
async def booking_page(request: Request, db: Session = Depends(get_db)):
    """صفحة الحجز"""
    services = db.query(models.Service).filter(models.Service.is_active == True).order_by(models.Service.price).all()
    characters = db.query(models.Character).filter(models.Character.is_available == True).all()
    ctx = {
        "request": request,
        "services": services,
        "characters": characters,
        "active_page": "booking",
        **get_global_context(db),
    }
    return templates.TemplateResponse(request, "booking.html", ctx)


@app.get("/contact", response_class=HTMLResponse)
async def contact_page(request: Request, db: Session = Depends(get_db)):
    """صفحة التواصل"""
    ctx = {
        "request": request,
        "active_page": "contact",
        **get_global_context(db),
    }
    return templates.TemplateResponse(request, "contact.html", ctx)


# ============ Admin Routes ============
@app.get("/admin/login", response_class=HTMLResponse)
async def admin_login_page(request: Request, db: Session = Depends(get_db)):
    """صفحة تسجيل دخول الأدمن"""
    ctx = {"request": request, **get_global_context(db), "error": None}
    return templates.TemplateResponse(request, "admin_login.html", ctx)


@app.post("/admin/login")
async def admin_login(
    request: Request,
    username: str = Form(...),
    password: str = Form(...),
    db: Session = Depends(get_db),
):
    """معالجة تسجيل دخول الأدمن"""
    user = db.query(models.User).filter(models.User.username == username).first()
    if not user or not verify_password(password, user.hashed_password) or not user.is_admin:
        ctx = {
            "request": request,
            **get_global_context(db),
            "error": "اسم المستخدم أو كلمة المرور غير صحيحة",
        }
        return templates.TemplateResponse(request, "admin_login.html", ctx, status_code=401)
    token = create_access_token({"sub": user.username})
    response = RedirectResponse(url="/admin", status_code=303)
    response.set_cookie("admin_token", token, httponly=True, max_age=ACCESS_TOKEN_EXPIRE_HOURS * 3600)
    return response


@app.get("/admin/logout")
async def admin_logout():
    """تسجيل خروج الأدمن"""
    response = RedirectResponse(url="/admin/login", status_code=303)
    response.delete_cookie("admin_token")
    return response


@app.get("/admin", response_class=HTMLResponse)
async def admin_dashboard(
    request: Request,
    db: Session = Depends(get_db),
    user: Optional[models.User] = Depends(verify_admin),
):
    """لوحة تحكم الأدمن"""
    if not user:
        return RedirectResponse(url="/admin/login", status_code=303)

    bookings = db.query(models.Booking).order_by(desc(models.Booking.created_at)).limit(50).all()
    messages = db.query(models.ContactMessage).order_by(desc(models.ContactMessage.created_at)).limit(20).all()

    # إحصائيات
    total_bookings = db.query(models.Booking).count()
    pending_bookings = db.query(models.Booking).filter(models.Booking.status == "pending").count()
    confirmed_bookings = db.query(models.Booking).filter(models.Booking.status == "confirmed").count()
    total_revenue = db.query(func.sum(models.Booking.total_price)).filter(models.Booking.status.in_(["confirmed", "completed"])).scalar() or 0
    unread_messages = db.query(models.ContactMessage).filter(models.ContactMessage.is_read == False).count()

    stats = {
        "total_bookings": total_bookings,
        "pending_bookings": pending_bookings,
        "confirmed_bookings": confirmed_bookings,
        "total_revenue": int(total_revenue),
        "unread_messages": unread_messages,
        "total_characters": db.query(models.Character).count(),
        "total_gallery": db.query(models.GalleryItem).count(),
    }

    ctx = {
        "request": request,
        "user": user,
        "bookings": bookings,
        "messages": messages,
        "stats": stats,
        **get_global_context(db),
    }
    return templates.TemplateResponse(request, "admin_dashboard.html", ctx)


# ============ API Endpoints ============

@app.get("/api/services", response_model=List[schemas.ServiceOut])
def api_get_services(db: Session = Depends(get_db)):
    """الحصول على كل الخدمات"""
    return db.query(models.Service).filter(models.Service.is_active == True).order_by(models.Service.price).all()


@app.get("/api/characters", response_model=List[schemas.CharacterOut])
def api_get_characters(category: Optional[str] = None, db: Session = Depends(get_db)):
    """الحصول على الشخصيات (مع فلترة اختيارية)"""
    q = db.query(models.Character).filter(models.Character.is_available == True)
    if category and category != "all":
        q = q.filter(models.Character.category == category)
    return q.all()


@app.get("/api/gallery", response_model=List[schemas.GalleryItemOut])
def api_get_gallery(category: Optional[str] = None, db: Session = Depends(get_db)):
    """الحصول على عناصر المعرض"""
    q = db.query(models.GalleryItem)
    if category and category != "all":
        q = q.filter(models.GalleryItem.category == category)
    return q.order_by(desc(models.GalleryItem.created_at)).all()


@app.get("/api/testimonials", response_model=List[schemas.TestimonialOut])
def api_get_testimonials(db: Session = Depends(get_db)):
    """الحصول على شهادات العملاء"""
    return db.query(models.Testimonial).filter(models.Testimonial.is_featured == True).all()


@app.post("/api/bookings", response_model=schemas.BookingOut)
def api_create_booking(payload: schemas.BookingCreate, db: Session = Depends(get_db)):
    """إنشاء حجز جديد"""
    # تحويل التاريخ
    try:
        event_date = datetime.strptime(payload.event_date, "%Y-%m-%d")
    except ValueError:
        raise HTTPException(status_code=400, detail="تنسيق التاريخ غير صحيح. استخدم YYYY-MM-DD")

    # حساب السعر النهائي إذا لم يُمرر
    total_price = payload.total_price
    if total_price <= 0:
        if payload.service_id:
            service = db.query(models.Service).filter(models.Service.id == payload.service_id).first()
            if service:
                total_price = service.price
        # إضافة سعر الشخصيات
        for cid in payload.characters_ids:
            char = db.query(models.Character).filter(models.Character.id == cid).first()
            if char:
                total_price += char.price_per_hour * 2  # افتراضي ساعتين

    booking = models.Booking(
        booking_code=generate_booking_code(),
        customer_name=payload.customer_name,
        customer_phone=payload.customer_phone,
        customer_email=payload.customer_email,
        event_type=payload.event_type,
        event_date=event_date,
        event_time=payload.event_time,
        location=payload.location,
        city=payload.city,
        kids_count=payload.kids_count,
        age_group=payload.age_group,
        service_id=payload.service_id,
        characters_ids=payload.characters_ids,
        extras=payload.extras,
        notes=payload.notes,
        total_price=total_price,
        deposit_amount=total_price * 0.3,  # 30% عربون
        status="pending",
        payment_status="unpaid",
    )
    db.add(booking)
    db.commit()
    db.refresh(booking)

    # زيادة شهرة الشخصيات المختارة
    for cid in payload.characters_ids:
        char = db.query(models.Character).filter(models.Character.id == cid).first()
        if char:
            char.popularity += 1
    db.commit()

    return booking


@app.get("/api/bookings/{booking_code}", response_model=schemas.BookingOut)
def api_get_booking(booking_code: str, db: Session = Depends(get_db)):
    """البحث عن حجز برمز الحجز"""
    booking = db.query(models.Booking).filter(models.Booking.booking_code == booking_code).first()
    if not booking:
        raise HTTPException(status_code=404, detail="الحجز غير موجود")
    return booking


@app.post("/api/contact", response_model=schemas.ContactMessageOut)
def api_create_contact(payload: schemas.ContactMessageCreate, db: Session = Depends(get_db)):
    """إرسال رسالة تواصل"""
    msg = models.ContactMessage(**payload.dict())
    db.add(msg)
    db.commit()
    db.refresh(msg)
    return msg


@app.get("/api/stats", response_model=schemas.HomeStats)
def api_stats(db: Session = Depends(get_db)):
    """إحصائيات عامة"""
    return schemas.HomeStats(
        total_bookings=db.query(models.Booking).count() + 247,
        total_characters=db.query(models.Character).count(),
        total_gallery=db.query(models.GalleryItem).count(),
        happy_clients=max(db.query(models.Booking).count() + 247, 250),
    )


# ============ Admin API ============
@app.post("/api/admin/bookings/{booking_id}/status")
def admin_update_booking_status(
    booking_id: int,
    status_value: str = Form(...),
    db: Session = Depends(get_db),
    user: Optional[models.User] = Depends(verify_admin),
):
    """تحديث حالة الحجز - للأدمن فقط"""
    if not user:
        raise HTTPException(status_code=401, detail="غير مصرح")
    booking = db.query(models.Booking).filter(models.Booking.id == booking_id).first()
    if not booking:
        raise HTTPException(status_code=404, detail="الحجز غير موجود")
    if status_value not in ["pending", "confirmed", "completed", "cancelled"]:
        raise HTTPException(status_code=400, detail="حالة غير صحيحة")
    booking.status = status_value
    db.commit()
    return {"success": True, "status": booking.status}


@app.get("/api/health")
def health_check():
    """فحص صحة التطبيق"""
    return {"status": "ok", "message": "🎉 Party Magic API is running!"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
