from django.contrib import admin
from django.contrib.auth.models import User
from django.contrib.auth.admin import UserAdmin
from django.db.models import Count
from django.core.exceptions import PermissionDenied
from django.template.response import TemplateResponse
from django.urls import path, reverse
from .models import ArticleCategory, Article, News, Page, ContactMessage, FAQ, Tag
from jobs.models import JobVacancy, JobLocation, Category as JobCategory, Skill, JobApplication
from users.models import JobSeekerProfile, EmployerProfile

# Переопределяем view административной главной страницы для подсчета статистики
class CustomAdminSite(admin.AdminSite):
    site_header = "Панель администратора службы занятости"
    site_title = "Администрирование сайта"
    index_title = "Управление сайтом"
    
    def _build_app_dict(self, request, label=None):
        """
        Переопределяем метод для добавления правильных URL
        """
        app_dict = super()._build_app_dict(request, label)
        return app_dict
    
    def get_app_list(self, request):
        """
        Возвращаем список приложений, включая модели и URL для админки
        """
        # Сначала получаем стандартный список приложений
        app_dict = self._build_app_dict(request)
        app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())
        
        return app_list
    
    def index(self, request, extra_context=None):
        if not request.user.is_staff:
            raise PermissionDenied
        
        # Статистика для главной страницы админки
        vacancy_count = JobVacancy.objects.count()
        user_count = User.objects.count()
        employer_count = EmployerProfile.objects.count()
        jobseeker_count = JobSeekerProfile.objects.count()
        article_count = Article.objects.count()
        news_count = News.objects.count()
        message_count = ContactMessage.objects.count()
        
        context = {
            'vacancy_count': vacancy_count,
            'user_count': user_count,
            'employer_count': employer_count,
            'jobseeker_count': jobseeker_count,
            'article_count': article_count,
            'news_count': news_count,
            'content_count': article_count + news_count,
            'message_count': message_count,
            **(extra_context or {}),
        }
        
        return super().index(request, context)

# Заменяем стандартный AdminSite на наш кастомный
admin_site = CustomAdminSite(name='admin')

# Регистрация стандартных моделей
from django.contrib.auth.models import User, Group
from django.contrib.auth.admin import UserAdmin, GroupAdmin
admin_site.register(User, UserAdmin)
admin_site.register(Group, GroupAdmin)

# Переопределяем admin.site глобально
admin.site = admin_site

# Класс для категорий статей
class ArticleCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'get_articles_count')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)
    
    def get_articles_count(self, obj):
        return obj.articles.count()
    get_articles_count.short_description = 'Статей'
    
    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(articles_count=Count('articles'))
        return queryset

# Класс для тегов
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

# Класс для статей
class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'author', 'created_at', 'is_published', 'views')
    list_filter = ('is_published', 'category', 'created_at', 'tags')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    list_editable = ('is_published',)
    readonly_fields = ('created_at', 'updated_at', 'views')
    filter_horizontal = ('tags',)
    save_on_top = True
    list_per_page = 20
    actions = ['make_published', 'make_unpublished']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'slug', 'category', 'content', 'image')
        }),
        ('Публикация', {
            'fields': ('author', 'is_published', 'created_at', 'updated_at')
        }),
        ('Дополнительно', {
            'fields': ('tags', 'views'),
            'classes': ('collapse',),
        }),
    )
    
    def make_published(self, request, queryset):
        queryset.update(is_published=True)
    make_published.short_description = "Опубликовать выбранные статьи"
    
    def make_unpublished(self, request, queryset):
        queryset.update(is_published=False)
    make_unpublished.short_description = "Снять с публикации выбранные статьи"
    
    def save_model(self, request, obj, form, change):
        if not obj.author_id:
            obj.author = request.user
        super().save_model(request, obj, form, change)

# Класс для новостей
class NewsAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'created_at', 'is_published', 'views')
    list_filter = ('is_published', 'created_at')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    list_editable = ('is_published',)
    readonly_fields = ('created_at', 'updated_at', 'views')
    save_on_top = True
    actions = ['make_published', 'make_unpublished']
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'slug', 'content', 'image')
        }),
        ('Публикация', {
            'fields': ('author', 'is_published', 'created_at', 'updated_at')
        }),
        ('Дополнительно', {
            'fields': ('views',),
            'classes': ('collapse',),
        }),
    )
    
    def make_published(self, request, queryset):
        queryset.update(is_published=True)
    make_published.short_description = "Опубликовать выбранные новости"
    
    def make_unpublished(self, request, queryset):
        queryset.update(is_published=False)
    make_unpublished.short_description = "Снять с публикации выбранные новости"
    
    def save_model(self, request, obj, form, change):
        if not obj.author_id:
            obj.author = request.user
        super().save_model(request, obj, form, change)

# Класс для страниц
class PageAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_published', 'is_in_menu', 'menu_order', 'created_at')
    list_filter = ('is_published', 'is_in_menu')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('is_published', 'is_in_menu', 'menu_order')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Основная информация', {
            'fields': ('title', 'slug', 'content')
        }),
        ('Настройки страницы', {
            'fields': ('is_published', 'is_in_menu', 'menu_order')
        }),
        ('Даты', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        }),
    )

# Класс для сообщений обратной связи
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    readonly_fields = ('name', 'email', 'subject', 'message', 'created_at')
    date_hierarchy = 'created_at'
    list_editable = ('status',)
    
    fieldsets = (
        ('Информация о сообщении', {
            'fields': ('name', 'email', 'subject', 'message', 'created_at')
        }),
        ('Обработка', {
            'fields': ('status', 'response', 'responded_by', 'responded_at')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if 'response' in form.changed_data:
            obj.responded_by = request.user
        super().save_model(request, obj, form, change)

# Класс для FAQ
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'category', 'order', 'is_published')
    list_filter = ('category', 'is_published')
    search_fields = ('question', 'answer')
    list_editable = ('order', 'is_published')
    fieldsets = (
        ('Вопрос и ответ', {
            'fields': ('question', 'answer')
        }),
        ('Настройки', {
            'fields': ('category', 'order', 'is_published')
        }),
    )

# Регистрация моделей в admin_site
admin_site.register(ArticleCategory, ArticleCategoryAdmin)
admin_site.register(Tag, TagAdmin)
admin_site.register(Article, ArticleAdmin)
admin_site.register(News, NewsAdmin)
admin_site.register(Page, PageAdmin)
admin_site.register(ContactMessage, ContactMessageAdmin)
admin_site.register(FAQ, FAQAdmin)
