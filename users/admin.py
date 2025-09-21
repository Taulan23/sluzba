from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import User
from .models import JobSeekerProfile, EmployerProfile
from core.admin import admin_site

# Расширяем стандартный UserAdmin, чтобы отображать связанные профили
class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'is_active', 'get_profile_type')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    
    def get_profile_type(self, obj):
        if hasattr(obj, 'job_seeker_profile'):
            return 'Соискатель'
        elif hasattr(obj, 'employer_profile'):
            return 'Работодатель'
        else:
            return 'Нет профиля'
    get_profile_type.short_description = 'Тип профиля'

# Класс администратора для профилей соискателей
class JobSeekerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'get_full_name', 'phone_number', 'created_at', 'is_active')
    search_fields = ('user__username', 'user__email', 'phone_number', 'user__first_name', 'user__last_name')
    list_filter = ('created_at', 'updated_at', 'user__is_active')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 20
    
    fieldsets = (
        ('Пользователь', {
            'fields': ('user',)
        }),
        ('Личная информация', {
            'fields': ('photo', 'birth_date', 'phone_number')
        }),
        ('Профессиональная информация', {
            'fields': ('skills', 'education', 'experience', 'resume_file')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def get_full_name(self, obj):
        return f"{obj.user.first_name} {obj.user.last_name}".strip() or obj.user.username
    get_full_name.short_description = 'Полное имя'
    
    def is_active(self, obj):
        return obj.user.is_active
    is_active.boolean = True
    is_active.short_description = 'Активен'

# Класс администратора для профилей работодателей
class EmployerProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'company_name', 'company_phone', 'created_at', 'is_active', 'vacancy_count')
    search_fields = ('user__username', 'user__email', 'company_name', 'company_phone')
    list_filter = ('created_at', 'updated_at', 'user__is_active')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 20
    
    fieldsets = (
        ('Пользователь', {
            'fields': ('user',)
        }),
        ('Информация о компании', {
            'fields': ('company_name', 'company_phone', 'company_website', 'company_logo')
        }),
        ('Описание и контакты', {
            'fields': ('company_description', 'company_address', 'company_email')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def is_active(self, obj):
        return obj.user.is_active
    is_active.boolean = True
    is_active.short_description = 'Активен'
    
    def vacancy_count(self, obj):
        return obj.vacancies.count() if hasattr(obj, 'vacancies') else 0
    vacancy_count.short_description = 'Вакансий'

# Перерегистрация User с нашим кастомным UserAdmin
admin_site.unregister(User)
admin_site.register(User, UserAdmin)

# Регистрация моделей в admin_site
admin_site.register(JobSeekerProfile, JobSeekerProfileAdmin)
admin_site.register(EmployerProfile, EmployerProfileAdmin)
