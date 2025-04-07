# Mausomi_Bazzar

একটি মডার্ন ইকমার্স প্ল্যাটফর্ম যা Django দিয়ে তৈরি করা হয়েছে।

## প্রজেক্টের ফিচারসমূহ

### 1. ইউজার ম্যানেজমেন্ট (accounts)
- কাস্টম ইউজার মডেল
- রেজিস্ট্রেশন এবং লগইন সিস্টেম
- প্রোফাইল ম্যানেজমেন্ট
- পাসওয়ার্ড রিসেট

### 2. প্রোডাক্ট ম্যানেজমেন্ট (products)
- প্রোডাক্ট ক্যাটাগরি
- প্রোডাক্ট লিস্টিং
- প্রোডাক্ট সার্চ
- প্রোডাক্ট ফিল্টারিং

### 3. অর্ডার ম্যানেজমেন্ট (orders)
- অর্ডার প্লেসমেন্ট
- অর্ডার ট্র্যাকিং
- পেমেন্ট প্রসেসিং

### 4. কার্ট সিস্টেম (cart)
- শপিং কার্ট
- চেকআউট প্রসেস

### 5. API (api)
- REST API এন্ডপয়েন্টস
- API ডকুমেন্টেশন

## টেকনোলজি স্ট্যাক
- Django 4.2
- PostgreSQL
- Django REST Framework
- Bootstrap 5

## ইনস্টলেশন
```bash
# ভার্চুয়াল এনভায়রনমেন্ট তৈরি
python -m venv venv

# ভার্চুয়াল এনভায়রনমেন্ট অ্যাক্টিভেট
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate  # Windows

# প্যাকেজ ইনস্টল
pip install -r requirements.txt

# মাইগ্রেশন
python manage.py migrate

# সার্ভার রান
python manage.py runserver
``` 