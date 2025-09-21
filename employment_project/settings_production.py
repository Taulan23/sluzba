"""
Настройки для продакшена
"""
import os
from .settings import *

# Безопасность
DEBUG = False
SECRET_KEY = os.environ.get('SECRET_KEY', 'django-insecure-!_z3=d*ar3a7b2$^%iparfbrj1r37nr4ww(^%p$1hvb&pom&k*')

# Временно включаем DEBUG для отладки
if os.environ.get('RENDER'):
    DEBUG = True
    print(f"RENDER environment detected. DEBUG={DEBUG}")
    print(f"ALLOWED_HOSTS={ALLOWED_HOSTS}")

# Разрешенные хосты - упрощенная версия для Render
ALLOWED_HOSTS = ['*']  # Разрешаем все домены для отладки

# Упрощенная логика для Render
if os.environ.get('RENDER'):
    ALLOWED_HOSTS = ['*']  # Разрешаем все домены

# База данных для продакшена
if os.environ.get('DATABASE_URL'):
    import dj_database_url
    DATABASES = {
        'default': dj_database_url.parse(os.environ.get('DATABASE_URL'))
    }
else:
    # Fallback на SQLite для Render
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

# Статические файлы
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Настройки для Render
if os.environ.get('RENDER'):
    # Используем whitenoise для статических файлов на Render
    MIDDLEWARE.insert(1, 'whitenoise.middleware.WhiteNoiseMiddleware')
    STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# Медиа файлы
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Безопасность
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'

# Логирование
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'root': {
        'handlers': ['console'],
    },
}
