"""
نماذج قاعدة البيانات - Database Models
يحتوي على كل الجداول المطلوبة للموقع:
- Services: الخدمات والباقات
- Characters: الشخصيات والماسكات
- Bookings: الحجوزات
- Gallery: صور المعرض
- Testimonials: شهادات العملاء
- Users: المستخدمين والأدمن
- Messages: رسائل التواصل
"""
from sqlalchemy import (
    Column, Integer, String, Float, Boolean, DateTime, Text, ForeignKey, JSON
)
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base


class Service(Base):
    """جدول الخدمات والباقات (أساسي / متقدم / VIP / إلخ)"""
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    name_ar = Column(String(200), nullable=False)        # اسم الخدمة بالعربية
    name_en = Column(String(200), nullable=True)         # اسم الخدمة بالإنجليزية
    slug = Column(String(200), unique=True, index=True)  # رابط فريد
    description = Column(Text, nullable=False)           # الوصف
    short_desc = Column(String(300), nullable=True)      # وصف مختصر
    price = Column(Float, nullable=False)                # السعر بالجنيه
    duration_hours = Column(Float, default=2.0)          # مدة الحفلة بالساعات
    icon = Column(String(50), default="🎉")              # رمز إيموجي
    image_url = Column(String(500), nullable=True)       # رابط الصورة الرئيسية
    features = Column(JSON, default=list)                # قائمة المميزات (JSON)
    category = Column(String(50), default="birthday")    # birthday | sebou | mascot | decoration
    is_popular = Column(Boolean, default=False)          # هل الباقة الأكثر شعبية؟
    is_active = Column(Boolean, default=True)            # حالة التفعيل
    order = Column(Integer, default=0)                   # ترتيب العرض
    created_at = Column(DateTime, default=datetime.utcnow)


class Character(Base):
    """جدول الشخصيات والماسكات (سبونج بوب، إلسا، سبايدرمان...)"""
    __tablename__ = "characters"

    id = Column(Integer, primary_key=True, index=True)
    name_ar = Column(String(200), nullable=False)        # اسم الشخصية بالعربية
    name_en = Column(String(200), nullable=True)         # اسم الشخصية بالإنجليزية
    slug = Column(String(200), unique=True, index=True)  # رابط فريد
    description = Column(Text, nullable=True)            # وصف الشخصية
    image_url = Column(String(500), nullable=False)      # رابط الصورة
    category = Column(String(50), default="cartoon")     # cartoon | princess | superhero | animal
    price_per_hour = Column(Float, default=500.0)        # السعر للساعة
    is_available = Column(Boolean, default=True)         # متاحة للحجز؟
    is_featured = Column(Boolean, default=False)         # شخصية مميزة؟
    color_theme = Column(String(20), default="#FF6B6B")  # لون الشخصية
    popularity = Column(Integer, default=0)              # عدد مرات الحجز
    created_at = Column(DateTime, default=datetime.utcnow)


class Booking(Base):
    """جدول الحجوزات"""
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    booking_code = Column(String(20), unique=True, index=True)  # كود الحجز (PRTY-XXXX)

    # بيانات العميل
    customer_name = Column(String(200), nullable=False)
    customer_phone = Column(String(20), nullable=False)
    customer_email = Column(String(200), nullable=True)

    # بيانات الحفلة
    event_type = Column(String(50), nullable=False)       # birthday | sebou | other
    event_date = Column(DateTime, nullable=False)         # تاريخ ووقت الحفلة
    event_time = Column(String(20), nullable=True)        # وقت الحفلة
    location = Column(String(500), nullable=False)        # العنوان
    city = Column(String(100), default="القاهرة")        # المدينة
    kids_count = Column(Integer, default=10)             # عدد الأطفال
    age_group = Column(String(50), nullable=True)        # الفئة العمرية

    # الباقة والشخصيات
    service_id = Column(Integer, ForeignKey("services.id"), nullable=True)
    characters_ids = Column(JSON, default=list)          # قائمة IDs للشخصيات

    # الإضافات والملاحظات
    extras = Column(JSON, default=list)                  # إضافات (تصوير، كيك، ...)
    notes = Column(Text, nullable=True)                  # ملاحظات إضافية

    # السعر والحالة
    total_price = Column(Float, default=0.0)
    deposit_amount = Column(Float, default=0.0)
    status = Column(String(20), default="pending")        # pending|confirmed|completed|cancelled
    payment_status = Column(String(20), default="unpaid") # unpaid | partial | paid

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    service = relationship("Service")


class GalleryItem(Base):
    """جدول صور ومقاطع المعرض"""
    __tablename__ = "gallery"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=True)           # عنوان الصورة
    description = Column(Text, nullable=True)            # وصف
    image_url = Column(String(500), nullable=False)      # رابط الصورة
    thumbnail_url = Column(String(500), nullable=True)   # رابط الصورة المصغرة
    category = Column(String(50), default="birthday")    # birthday|sebou|mascot|decoration
    is_featured = Column(Boolean, default=False)
    order = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.utcnow)


class Testimonial(Base):
    """جدول شهادات العملاء"""
    __tablename__ = "testimonials"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String(200), nullable=False)
    customer_role = Column(String(200), nullable=True)   # مثل: أم لطفلين
    avatar_url = Column(String(500), nullable=True)      # صورة العميل
    rating = Column(Integer, default=5)                  # تقييم 1-5
    content = Column(Text, nullable=False)               # نص الشهادة
    event_type = Column(String(50), nullable=True)
    is_featured = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class User(Base):
    """جدول المستخدمين والأدمن"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True)
    email = Column(String(200), unique=True, index=True)
    hashed_password = Column(String(500), nullable=False)
    full_name = Column(String(200), nullable=True)
    is_admin = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)


class ContactMessage(Base):
    """جدول رسائل التواصل من نموذج Contact"""
    __tablename__ = "contact_messages"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    phone = Column(String(20), nullable=True)
    email = Column(String(200), nullable=True)
    subject = Column(String(300), nullable=True)
    message = Column(Text, nullable=False)
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
