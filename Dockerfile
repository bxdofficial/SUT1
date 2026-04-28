# 🎉 Party Magic - Dockerfile
FROM python:3.11-slim

WORKDIR /app

# تثبيت اعتماديات النظام
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# نسخ ملف الاعتماديات وتثبيتها
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# نسخ الكود
COPY . .

# مجلد التحميلات
RUN mkdir -p /app/uploads

EXPOSE 8000

# تشغيل التطبيق
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8000"]
