# Accounts App

এই অ্যাপটি ইউজার অথেনটিকেশন এবং প্রোফাইল ম্যানেজমেন্টের জন্য ব্যবহৃত হয়।

## ফিচারসমূহ

### 1. ইউজার রেজিস্ট্রেশন
- ইমেইল ভিত্তিক রেজিস্ট্রেশন
- পাসওয়ার্ড ভেরিফিকেশন
- অটোমেটিক প্রোফাইল ক্রিয়েশন

### 2. ইউজার লগইন
- ইমেইল এবং পাসওয়ার্ড দিয়ে লগইন
- JWT টোকেন ভিত্তিক অথেনটিকেশন
- টোকেন রিফ্রেশ মেকানিজম

### 3. প্রোফাইল ম্যানেজমেন্ট
- প্রোফাইল তথ্য দেখা
- প্রোফাইল তথ্য আপডেট
- প্রোফাইল পিকচার আপলোড

### 4. পাসওয়ার্ড ম্যানেজমেন্ট
- পাসওয়ার্ড পরিবর্তন
- পাসওয়ার্ড ভেরিফিকেশন

## API এন্ডপয়েন্টস

### অথেনটিকেশন
- `POST /api/auth/register/`: নতুন ইউজার রেজিস্ট্রেশন
- `POST /api/auth/login/`: ইউজার লগইন
- `POST /api/auth/change-password/`: পাসওয়ার্ড পরিবর্তন

### প্রোফাইল
- `GET /api/profile/`: প্রোফাইল তথ্য দেখা
- `PATCH /api/profile/update/`: প্রোফাইল তথ্য আপডেট

## ডেটা মডেল

### User মডেল
- ইমেইল (ইউনিক)
- প্রথম নাম
- শেষ নাম
- পাসওয়ার্ড (এনক্রিপ্টেড)

### Profile মডেল
- ফোন নম্বর
- ঠিকানা
- প্রোফাইল পিকচার

## সিকিউরিটি ফিচার
- পাসওয়ার্ড এনক্রিপশন
- JWT টোকেন ভেরিফিকেশন
- সেশন ম্যানেজমেন্ট

## ব্যবহারের উদাহরণ

### রেজিস্ট্রেশন
```json
POST /api/auth/register/
{
    "email": "user@example.com",
    "password": "securepassword",
    "first_name": "John",
    "last_name": "Doe"
}
```

### লগইন
```json
POST /api/auth/login/
{
    "email": "user@example.com",
    "password": "securepassword"
}
```

### প্রোফাইল আপডেট
```json
PATCH /api/profile/update/
{
    "email": "newemail@example.com",
    "first_name": "John",
    "last_name": "Doe",
    "phone": "1234567890",
    "address": "123 Main St",
    "profile_picture": <file>
}
```

### পাসওয়ার্ড পরিবর্তন
```json
POST /api/auth/change-password/
{
    "old_password": "oldpassword",
    "new_password": "newpassword",
    "confirm_password": "newpassword"
}
```

## ইনস্টলেশন

1. `requirements.txt` ফাইলে নিচের প্যাকেজগুলি যোগ করুন:
```
djangorestframework
djangorestframework-simplejwt
django-cors-headers
Pillow
```

2. `settings.py` ফাইলে নিচের কনফিগারেশনগুলি যোগ করুন:
```python
INSTALLED_APPS = [
    ...
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'accounts',
]

AUTH_USER_MODEL = 'accounts.User'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}
```

3. মাইগ্রেশন রান করুন:
```bash
python manage.py makemigrations
python manage.py migrate
``` 