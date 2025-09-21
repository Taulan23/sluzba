from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.contrib.auth.models import User

class ArticleCategory(models.Model):
    """Модель категории статей"""
    name = models.CharField(max_length=100, verbose_name='Название категории')
    slug = models.SlugField(unique=True, verbose_name='URL')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')

    class Meta:
        verbose_name = 'Категория статей'
        verbose_name_plural = 'Категории статей'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('core:article_category', kwargs={'slug': self.slug})


class Tag(models.Model):
    """Модель тега для статей"""
    name = models.CharField(max_length=50, verbose_name='Название тега')
    slug = models.SlugField(unique=True, verbose_name='URL')
    
    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'
        ordering = ['name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
        
    def get_absolute_url(self):
        return reverse('core:article_tag', kwargs={'slug': self.slug})


class Article(models.Model):
    """Модель статьи"""
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = models.SlugField(unique=True, verbose_name='URL')
    category = models.ForeignKey(ArticleCategory, on_delete=models.CASCADE, related_name='articles', verbose_name='Категория')
    content = models.TextField(verbose_name='Содержание')
    image = models.ImageField(upload_to='articles/', blank=True, null=True, verbose_name='Изображение')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='articles', verbose_name='Автор')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    views = models.PositiveIntegerField(default=0, verbose_name='Просмотры')
    tags = models.ManyToManyField(Tag, blank=True, related_name='articles', verbose_name='Теги')
    
    class Meta:
        verbose_name = 'Статья'
        verbose_name_plural = 'Статьи'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('core:article_detail', kwargs={'slug': self.slug})


class News(models.Model):
    """Модель новости"""
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = models.SlugField(unique=True, verbose_name='URL')
    content = models.TextField(verbose_name='Содержание')
    image = models.ImageField(upload_to='news/', blank=True, null=True, verbose_name='Изображение')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='news', verbose_name='Автор')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    views = models.PositiveIntegerField(default=0, verbose_name='Просмотры')

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('core:news_detail', kwargs={'slug': self.slug})


class Page(models.Model):
    """Модель статической страницы"""
    title = models.CharField(max_length=255, verbose_name='Заголовок')
    slug = models.SlugField(unique=True, verbose_name='URL')
    content = models.TextField(verbose_name='Содержание')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    is_in_menu = models.BooleanField(default=False, verbose_name='Отображать в меню')
    menu_order = models.PositiveIntegerField(default=0, verbose_name='Порядок в меню')

    class Meta:
        verbose_name = 'Страница'
        verbose_name_plural = 'Страницы'
        ordering = ['menu_order', 'title']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('core:page', kwargs={'slug': self.slug})


class ContactMessage(models.Model):
    """Модель контактного сообщения"""
    STATUS_CHOICES = (
        ('new', 'Новое'),
        ('in_progress', 'В обработке'),
        ('answered', 'Отвечено'),
        ('closed', 'Закрыто'),
    )
    
    name = models.CharField(max_length=100, verbose_name='Имя')
    email = models.EmailField(verbose_name='Email')
    subject = models.CharField(max_length=255, verbose_name='Тема')
    message = models.TextField(verbose_name='Сообщение')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='new', verbose_name='Статус')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    response = models.TextField(blank=True, null=True, verbose_name='Ответ')
    responded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='responded_messages', verbose_name='Ответил')
    responded_at = models.DateTimeField(blank=True, null=True, verbose_name='Дата ответа')

    class Meta:
        verbose_name = 'Контактное сообщение'
        verbose_name_plural = 'Контактные сообщения'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.name}: {self.subject}"


class FAQ(models.Model):
    """Модель часто задаваемого вопроса"""
    question = models.CharField(max_length=255, verbose_name='Вопрос')
    answer = models.TextField(verbose_name='Ответ')
    category = models.CharField(max_length=100, blank=True, null=True, verbose_name='Категория')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок')
    is_published = models.BooleanField(default=True, verbose_name='Опубликовано')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQ'
        ordering = ['order', 'question']

    def __str__(self):
        return self.question
