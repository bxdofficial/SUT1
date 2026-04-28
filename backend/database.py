"""
إعدادات قاعدة البيانات - Database Configuration
استخدام SQLAlchemy 2.0 مع SQLite للتطوير المحلي (يمكن استبدالها بـ PostgreSQL للإنتاج)
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import os

# مسار قاعدة البيانات - SQLite ملف محلي
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "party.db")
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

# إنشاء المحرك مع تفعيل المفاتيح الأجنبية لـ SQLite
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},  # ضروري للـ SQLite
    echo=False,
)

# جلسة قاعدة البيانات
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# الكلاس الأساسي للموديلات
Base = declarative_base()


def get_db():
    """دالة Dependency لحقن جلسة قاعدة البيانات في الـ endpoints"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
