from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify

class JobSeekerProfile(models.Model):
    """Модель профиля соискателя"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='job_seeker_profile')
    photo = models.ImageField(upload_to='job_seekers/', blank=True, null=True, verbose_name='Фотография')
    birth_date = models.DateField(blank=True, null=True, verbose_name='Дата рождения')
    phone_number = models.CharField(max_length=20, blank=True, null=True, verbose_name='Номер телефона')
    education = models.TextField(blank=True, null=True, verbose_name='Образование')
    skills = models.TextField(blank=True, null=True, verbose_name='Навыки')
    experience = models.TextField(blank=True, null=True, verbose_name='Опыт работы')
    resume_file = models.FileField(upload_to='resumes/', blank=True, null=True, verbose_name='Файл резюме')
    slug = models.SlugField(unique=True, blank=True, verbose_name='URL')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Профиль соискателя'
        verbose_name_plural = 'Профили соискателей'
        ordering = ['-created_at']

    def __str__(self):
        return f'Профиль соискателя: {self.user.username}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.user.username}-{self.user.id}")
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('users:job_seeker_profile', kwargs={'slug': self.slug})


class EmployerProfile(models.Model):
    """Модель профиля работодателя"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employer_profile')
    company_name = models.CharField(max_length=255, verbose_name='Название компании')
    company_logo = models.ImageField(upload_to='employers/', blank=True, null=True, verbose_name='Логотип компании')
    company_description = models.TextField(blank=True, null=True, verbose_name='Описание компании')
    company_website = models.URLField(blank=True, null=True, verbose_name='Веб-сайт компании')
    company_address = models.CharField(max_length=255, blank=True, null=True, verbose_name='Адрес компании')
    company_phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Телефон компании')
    company_email = models.EmailField(blank=True, null=True, verbose_name='Email компании')
    slug = models.SlugField(unique=True, blank=True, verbose_name='URL')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Профиль работодателя'
        verbose_name_plural = 'Профили работодателей'
        ordering = ['-created_at']

    def __str__(self):
        return f'Профиль работодателя: {self.company_name}'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f"{self.company_name}-{self.user.id}")
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('users:employer_profile', kwargs={'slug': self.slug})
