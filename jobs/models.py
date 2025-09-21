from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from users.models import EmployerProfile, JobSeekerProfile
import uuid
import datetime

class Category(models.Model):
    """Модель категории вакансий"""
    name = models.CharField(max_length=100, verbose_name='Название категории')
    slug = models.SlugField(unique=True, verbose_name='URL')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')
    icon = models.CharField(max_length=50, blank=True, null=True, verbose_name='Иконка')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('jobs:category', kwargs={'slug': self.slug})


class Skill(models.Model):
    """Модель навыка"""
    name = models.CharField(max_length=100, unique=True, verbose_name='Название навыка')
    slug = models.SlugField(unique=True, verbose_name='URL')
    description = models.TextField(blank=True, null=True, verbose_name='Описание')

    class Meta:
        verbose_name = 'Навык'
        verbose_name_plural = 'Навыки'
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class JobLocation(models.Model):
    """Модель местоположения работы"""
    city = models.CharField(max_length=100, verbose_name='Город')
    region = models.CharField(max_length=100, verbose_name='Регион')
    address = models.CharField(max_length=255, blank=True, null=True, verbose_name='Адрес')

    class Meta:
        verbose_name = 'Местоположение'
        verbose_name_plural = 'Местоположения'
        ordering = ['city', 'region']
        unique_together = ['city', 'region', 'address']

    def __str__(self):
        return f"{self.city}, {self.region}"


class JobVacancy(models.Model):
    """Модель вакансии"""
    # Статусы вакансии
    STATUS_CHOICES = (
        ('open', 'Открыта'),
        ('closed', 'Закрыта'),
        ('archived', 'В архиве'),
    )
    
    # Тип занятости
    EMPLOYMENT_TYPE_CHOICES = (
        ('full_time', 'Полная занятость'),
        ('part_time', 'Частичная занятость'),
        ('contract', 'Контракт'),
        ('internship', 'Стажировка'),
        ('remote', 'Удаленная работа'),
    )
    
    # Опыт работы
    EXPERIENCE_CHOICES = (
        ('no_experience', 'Без опыта'),
        ('1-3', '1-3 года'),
        ('3-5', '3-5 лет'),
        ('5+', 'Более 5 лет'),
    )
    
    title = models.CharField(max_length=255, verbose_name='Название вакансии')
    slug = models.SlugField(unique=True, verbose_name='URL')
    employer = models.ForeignKey(EmployerProfile, on_delete=models.CASCADE, related_name='vacancies', verbose_name='Работодатель')
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='vacancies', verbose_name='Категория')
    description = models.TextField(verbose_name='Описание вакансии')
    requirements = models.TextField(verbose_name='Требования')
    responsibilities = models.TextField(verbose_name='Обязанности')
    benefits = models.TextField(blank=True, null=True, verbose_name='Преимущества')
    salary_min = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='Минимальная зарплата')
    salary_max = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True, verbose_name='Максимальная зарплата')
    location = models.ForeignKey(JobLocation, on_delete=models.SET_NULL, blank=True, null=True, related_name='vacancies', verbose_name='Местоположение')
    is_remote = models.BooleanField(default=False, verbose_name='Удаленная работа')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open', verbose_name='Статус')
    employment_type = models.CharField(max_length=20, choices=EMPLOYMENT_TYPE_CHOICES, verbose_name='Тип занятости')
    experience_required = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES, verbose_name='Требуемый опыт')
    skills = models.ManyToManyField(Skill, related_name='vacancies', blank=True, verbose_name='Навыки')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    
    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            # Создаём базовый slug из названия вакансии и названия компании
            base_slug = slugify(f"{self.title}-{self.employer.company_name}")
            
            # Добавляем текущую дату для уникальности
            today = datetime.date.today().strftime('%Y%m%d')
            unique_id = str(uuid.uuid4())[:8]  # Берём первые 8 символов UUID
            
            # Создаём уникальный slug
            self.slug = f"{base_slug}-{today}-{unique_id}"
            
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('jobs:vacancy_detail', kwargs={'slug': self.slug})


class JobApplication(models.Model):
    """Модель заявки на вакансию"""
    STATUS_CHOICES = (
        ('pending', 'На рассмотрении'),
        ('reviewed', 'Рассмотрена'),
        ('interview', 'Приглашение на собеседование'),
        ('rejected', 'Отклонена'),
        ('accepted', 'Принята'),
    )
    
    job_seeker = models.ForeignKey(JobSeekerProfile, on_delete=models.CASCADE, related_name='applications', verbose_name='Соискатель')
    vacancy = models.ForeignKey(JobVacancy, on_delete=models.CASCADE, related_name='applications', verbose_name='Вакансия')
    cover_letter = models.TextField(blank=True, null=True, verbose_name='Сопроводительное письмо')
    resume_file = models.FileField(upload_to='job_applications/', blank=True, null=True, verbose_name='Файл резюме')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name='Статус')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    employer_notes = models.TextField(blank=True, null=True, verbose_name='Заметки работодателя')
    
    class Meta:
        verbose_name = 'Заявка на вакансию'
        verbose_name_plural = 'Заявки на вакансии'
        ordering = ['-created_at']
        unique_together = ['job_seeker', 'vacancy']
    
    def __str__(self):
        return f"Заявка от {self.job_seeker.user.username} на вакансию {self.vacancy.title}"
