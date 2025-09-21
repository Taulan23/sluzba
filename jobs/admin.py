from django.contrib import admin
from .models import Category, Skill, JobLocation, JobVacancy, JobApplication
from core.admin import admin_site

# Класс администратора для категорий
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    list_per_page = 20

# Класс администратора для навыков
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    list_per_page = 20

# Класс администратора для местоположений
class JobLocationAdmin(admin.ModelAdmin):
    list_display = ('city', 'region', 'address')
    search_fields = ('city', 'region', 'address')
    list_filter = ('region', 'city')
    list_per_page = 20

# Класс администратора для вакансий
class JobVacancyAdmin(admin.ModelAdmin):
    list_display = ('title', 'employer', 'category', 'salary_min', 'salary_max', 'status', 'created_at')
    list_filter = ('status', 'category', 'employment_type', 'experience_required', 'is_remote', 'created_at')
    search_fields = ('title', 'description', 'requirements', 'employer__company_name')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    filter_horizontal = ('skills',)
    list_editable = ('status',)
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 20
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'slug', 'description', 'requirements', 'responsibilities')
        }),
        ('Работодатель и категория', {
            'fields': ('employer', 'category', 'skills')
        }),
        ('Условия работы', {
            'fields': ('salary_min', 'salary_max', 'employment_type', 'experience_required', 'is_remote', 'location')
        }),
        ('Публикация', {
            'fields': ('status', 'created_at', 'updated_at')
        }),
    )
    
    actions = ['make_active', 'make_closed', 'make_draft']
    
    def make_active(self, request, queryset):
        queryset.update(status='open')
    make_active.short_description = "Опубликовать выбранные вакансии"
    
    def make_closed(self, request, queryset):
        queryset.update(status='closed')
    make_closed.short_description = "Закрыть выбранные вакансии"
    
    def make_draft(self, request, queryset):
        queryset.update(status='archived')
    make_draft.short_description = "Перевести выбранные вакансии в архив"

# Класс администратора для заявок на вакансии
class JobApplicationAdmin(admin.ModelAdmin):
    list_display = ('job_seeker', 'vacancy', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('job_seeker__user__username', 'vacancy__title', 'cover_letter')
    date_hierarchy = 'created_at'
    list_editable = ('status',)
    readonly_fields = ('created_at', 'updated_at')
    list_per_page = 20
    
    fieldsets = (
        ('Заявитель и вакансия', {
            'fields': ('job_seeker', 'vacancy')
        }),
        ('Детали заявки', {
            'fields': ('cover_letter', 'resume_file', 'status')
        }),
        ('Примечания', {
            'fields': ('employer_notes',)
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    actions = ['accept_applications', 'reject_applications', 'mark_as_reviewing']
    
    def accept_applications(self, request, queryset):
        queryset.update(status='accepted')
    accept_applications.short_description = "Принять выбранные заявки"
    
    def reject_applications(self, request, queryset):
        queryset.update(status='rejected')
    reject_applications.short_description = "Отклонить выбранные заявки"
    
    def mark_as_reviewing(self, request, queryset):
        queryset.update(status='reviewing')
    mark_as_reviewing.short_description = "Отметить выбранные заявки как 'На рассмотрении'"

# Регистрация моделей в admin_site
admin_site.register(Category, CategoryAdmin)
admin_site.register(Skill, SkillAdmin)
admin_site.register(JobLocation, JobLocationAdmin)
admin_site.register(JobVacancy, JobVacancyAdmin)
admin_site.register(JobApplication, JobApplicationAdmin)
