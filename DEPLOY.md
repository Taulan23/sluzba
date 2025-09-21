# 🚀 Деплой на Render.com

## Инструкция по деплою Django сайта службы занятости на Render.com

### 1. Подготовка GitHub репозитория

```bash
# Инициализация Git
git init
git add .
git commit -m "Initial commit for deployment"

# Создание репозитория на GitHub
# Загрузите код на GitHub
```

### 2. Деплой на Render.com

1. **Перейдите на [Render.com](https://dashboard.render.com/)**
2. **Войдите через GitHub**
3. **Нажмите "New +" → "Web Service"**
4. **Выберите ваш репозиторий**
5. **Настройте параметры:**

#### Настройки сервиса:
- **Name**: `employment-service`
- **Environment**: `Python 3`
- **Build Command**: 
  ```bash
  pip install -r requirements.txt && python manage.py collectstatic --noinput && python manage.py migrate
  ```
- **Start Command**: 
  ```bash
  gunicorn employment_project.wsgi:application
  ```

#### Переменные окружения:
- `DJANGO_SETTINGS_MODULE` = `employment_project.settings_production`
- `SECRET_KEY` = (сгенерируйте новый ключ)
- `RENDER` = `true`

### 3. Автоматический деплой

Render автоматически:
- ✅ Установит зависимости
- ✅ Соберет статические файлы
- ✅ Выполнит миграции
- ✅ Запустит сервер

### 4. Проверка деплоя

После успешного деплоя ваш сайт будет доступен по адресу:
`https://your-app-name.onrender.com`

### 5. Админ-панель

Создайте суперпользователя:
```bash
python manage.py createsuperuser
```

### 6. Особенности Render

- ✅ **750 часов бесплатно** в месяц
- ✅ Автоматический SSL
- ✅ Автоматический деплой при push в GitHub
- ✅ Встроенная поддержка Django
- ✅ Бесплатная PostgreSQL база данных

### 7. Мониторинг

- Логи доступны в панели Render
- Мониторинг производительности
- Автоматические уведомления об ошибках
