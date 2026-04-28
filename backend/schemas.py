"""
Pydantic Schemas للتحقق من البيانات
"""
from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime


# ============ Service Schemas ============
class ServiceBase(BaseModel):
    name_ar: str
    name_en: Optional[str] = None
    slug: str
    description: str
    short_desc: Optional[str] = None
    price: float
    duration_hours: float = 2.0
    icon: str = "🎉"
    image_url: Optional[str] = None
    features: List[str] = []
    category: str = "birthday"
    is_popular: bool = False


class ServiceCreate(ServiceBase):
    pass


class ServiceOut(ServiceBase):
    id: int
    is_active: bool
    order: int
    created_at: datetime

    class Config:
        from_attributes = True


# ============ Character Schemas ============
class CharacterBase(BaseModel):
    name_ar: str
    name_en: Optional[str] = None
    slug: str
    description: Optional[str] = None
    image_url: str
    category: str = "cartoon"
    price_per_hour: float = 500.0
    color_theme: str = "#FF6B6B"
    is_featured: bool = False


class CharacterCreate(CharacterBase):
    pass


class CharacterOut(CharacterBase):
    id: int
    is_available: bool
    popularity: int

    class Config:
        from_attributes = True


# ============ Booking Schemas ============
class BookingCreate(BaseModel):
    customer_name: str = Field(..., min_length=3, max_length=200)
    customer_phone: str = Field(..., min_length=10, max_length=20)
    customer_email: Optional[str] = None

    event_type: str  # birthday | sebou | other
    event_date: str  # YYYY-MM-DD
    event_time: Optional[str] = None
    location: str = Field(..., min_length=5)
    city: str = "القاهرة"
    kids_count: int = Field(default=10, ge=1, le=500)
    age_group: Optional[str] = None

    service_id: Optional[int] = None
    characters_ids: List[int] = []
    extras: List[str] = []
    notes: Optional[str] = None
    total_price: float = 0.0


class BookingOut(BaseModel):
    id: int
    booking_code: str
    customer_name: str
    customer_phone: str
    event_type: str
    event_date: datetime
    location: str
    kids_count: int
    total_price: float
    status: str
    payment_status: str
    created_at: datetime

    class Config:
        from_attributes = True


# ============ Gallery Schemas ============
class GalleryItemBase(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    image_url: str
    category: str = "birthday"
    is_featured: bool = False


class GalleryItemOut(GalleryItemBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ============ Testimonial Schemas ============
class TestimonialBase(BaseModel):
    customer_name: str
    customer_role: Optional[str] = None
    avatar_url: Optional[str] = None
    rating: int = 5
    content: str
    event_type: Optional[str] = None


class TestimonialOut(TestimonialBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ============ Contact Schemas ============
class ContactMessageCreate(BaseModel):
    name: str = Field(..., min_length=2, max_length=200)
    phone: Optional[str] = None
    email: Optional[str] = None
    subject: Optional[str] = None
    message: str = Field(..., min_length=5)


class ContactMessageOut(ContactMessageCreate):
    id: int
    is_read: bool
    created_at: datetime

    class Config:
        from_attributes = True


# ============ Auth Schemas ============
class UserLogin(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


# ============ Stats Schemas ============
class HomeStats(BaseModel):
    """إحصائيات الصفحة الرئيسية"""
    total_bookings: int
    total_characters: int
    total_gallery: int
    happy_clients: int
