from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import JobSeekerProfile, EmployerProfile


class UserRegistrationForm(UserCreationForm):
    """Форма регистрации пользователя"""
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email'})
    )
    first_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя'})
    )
    last_name = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Фамилия'})
    )
    
    USER_TYPE_CHOICES = [
        ('job_seeker', 'Соискатель'),
        ('employer', 'Работодатель'),
    ]
    
    user_type = forms.ChoiceField(
        choices=USER_TYPE_CHOICES,
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        required=True,
        label='Тип пользователя'
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2', 'user_type']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Имя пользователя'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['password1'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Пароль'})
        self.fields['password2'].widget.attrs.update({'class': 'form-control', 'placeholder': 'Подтверждение пароля'})


class JobSeekerProfileForm(forms.ModelForm):
    """Форма профиля соискателя"""
    birth_date = forms.DateField(
        label='Дата рождения',
        required=False,
        widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'})
    )
    
    class Meta:
        model = JobSeekerProfile
        fields = ['photo', 'birth_date', 'phone_number', 'education', 'skills', 'experience', 'resume_file']
        widgets = {
            'photo': forms.FileInput(attrs={'class': 'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Номер телефона'}),
            'education': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Образование', 'rows': 4}),
            'skills': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Навыки', 'rows': 4}),
            'experience': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Опыт работы', 'rows': 4}),
            'resume_file': forms.FileInput(attrs={'class': 'form-control'}),
        }


class EmployerProfileForm(forms.ModelForm):
    """Форма профиля работодателя"""
    class Meta:
        model = EmployerProfile
        fields = [
            'company_name', 'company_logo', 'company_description', 'company_website',
            'company_address', 'company_phone', 'company_email'
        ]
        widgets = {
            'company_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Название компании'}),
            'company_logo': forms.FileInput(attrs={'class': 'form-control'}),
            'company_description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Описание компании', 'rows': 4}),
            'company_website': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'Веб-сайт компании'}),
            'company_address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Адрес компании'}),
            'company_phone': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Телефон компании'}),
            'company_email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email компании'}),
        } 