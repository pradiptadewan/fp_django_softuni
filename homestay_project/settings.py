from pathlib import Path
import os

BASE_DIR = Path(__file__).resolve().parent.parent

# Secret key, pastikan untuk mengganti dengan yang lebih aman di produksi
SECRET_KEY = 'django-insecure-zv32!@2@n6l5a=*4-jl%!s(#(!wau(rs8xas1o(l85z2$%84#y'

# Debugging settings (Hanya diaktifkan di development, nonaktifkan di production)
DEBUG = True

ALLOWED_HOSTS = []

# Daftar aplikasi yang terinstal
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'homestay',
]

# Middleware yang digunakan oleh aplikasi
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  # Untuk static files di produksi
]

ROOT_URLCONF = 'homestay_project.urls'

# Pengaturan template
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],  # Menentukan folder template di project
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.static',
            ],
        },
    },
]

WSGI_APPLICATION = 'homestay_project.wsgi.application'

# Pengaturan database PostgreSQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'homestay_db_2',
        'USER': 'postgres',
        'PASSWORD': 'dewan123',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}

# Validasi password
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Pengaturan lokal dan waktu
LANGUAGE_CODE = 'id-id'  # Mengganti bahasa ke Bahasa Indonesia
TIME_ZONE = 'Asia/Jakarta'  # Mengganti zona waktu ke waktu Indonesia
USE_I18N = True
USE_TZ = True

# Pengaturan untuk file statis (CSS, JavaScript, Images)
STATIC_URL = '/static/'

# Pengaturan untuk folder statis lokal yang bisa diakses selama pengembangan
STATICFILES_DIRS = [ BASE_DIR / 'static',  # Folder ini untuk menyimpan file statis tambahan
]

# Folder tempat file statis siap di-deploy untuk produksi
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Pengaturan untuk file media (misalnya gambar yang diupload)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

# Pengaturan untuk ID otomatis pada model
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Pengaturan login
LOGIN_URL = 'login'  # Mengarahkan pengguna ke halaman login
LOGIN_REDIRECT_URL = 'profile'  # Setelah login, pengguna diarahkan ke halaman profile
