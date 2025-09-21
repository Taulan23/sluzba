from django import forms
from .models import JobVacancy, JobApplication, Category, Skill, JobLocation

class JobVacancyForm(forms.ModelForm):
    """Форма создания/редактирования вакансии"""
    title = forms.CharField(
        label='Название вакансии',
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Введите название вакансии'})
    )
    description = forms.CharField(
        label='Описание вакансии',
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Опишите вакансию', 'rows': 5})
    )
    requirements = forms.CharField(
        label='Требования',
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Укажите требования', 'rows': 5})
    )
    responsibilities = forms.CharField(
        label='Обязанности',
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Укажите обязанности', 'rows': 5})
    )
    benefits = forms.CharField(
        label='Преимущества',
        required=False,
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Укажите преимущества', 'rows': 5})
    )
    salary_min = forms.DecimalField(
        label='Минимальная зарплата',
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Укажите минимальную зарплату'})
    )
    salary_max = forms.DecimalField(
        label='Максимальная зарплата',
        required=False,
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Укажите максимальную зарплату'})
    )
    is_remote = forms.BooleanField(
        label='Удаленная работа',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )
    skills = forms.ModelMultipleChoiceField(
        label='Навыки',
        queryset=Skill.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={'class': 'form-control select2'})
    )
    
    class Meta:
        model = JobVacancy
        fields = [
            'title', 'category', 'description', 'requirements', 'responsibilities', 
            'benefits', 'salary_min', 'salary_max', 'location', 'is_remote', 
            'employment_type', 'experience_required', 'skills'
        ]
        widgets = {
            'category': forms.Select(attrs={'class': 'form-control'}),
            'location': forms.Select(attrs={'class': 'form-control'}),
            'employment_type': forms.Select(attrs={'class': 'form-control'}),
            'experience_required': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        self.employer_user = kwargs.pop('employer', None)
        super().__init__(*args, **kwargs)
        
        # Инициализация полей выбора с первыми элементами, если их нет в данных
        if not self.data.get('category') and Category.objects.exists():
            self.initial['category'] = Category.objects.first().pk
            
        if not self.data.get('employment_type'):
            self.initial['employment_type'] = 'full_time'
            
        if not self.data.get('experience_required'):
            self.initial['experience_required'] = 'no_experience'
            
        # Устанавливаем help_text для поля location
        self.fields['location'].help_text = 'Выберите местоположение или отметьте "Удаленная работа"'
        
    def clean(self):
        cleaned_data = super().clean()
        salary_min = cleaned_data.get('salary_min')
        salary_max = cleaned_data.get('salary_max')
        
        # Проверяем, чтобы минимальная зарплата не была больше максимальной
        if salary_min and salary_max and salary_min > salary_max:
            self.add_error('salary_min', 'Минимальная зарплата не может быть больше максимальной')
            
        # Если вакансия удаленная, местоположение не обязательно
        is_remote = cleaned_data.get('is_remote')
        location = cleaned_data.get('location')
        if not is_remote and not location:
            self.add_error('location', 'Укажите местоположение или отметьте "Удаленная работа"')
            
        return cleaned_data


class JobApplicationForm(forms.ModelForm):
    """Форма заявки на вакансию"""
    cover_letter = forms.CharField(
        label='Сопроводительное письмо',
        widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Введите сопроводительное письмо', 'rows': 5})
    )
    resume_file = forms.FileField(
        label='Файл резюме',
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = JobApplication
        fields = ['cover_letter', 'resume_file']


class JobSearchForm(forms.Form):
    """Форма поиска вакансий"""
    keywords = forms.CharField(
        label='Ключевые слова',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Поиск по названию, описанию...'}),
    )
    category = forms.ModelChoiceField(
        label='Категория',
        queryset=Category.objects.all(),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    location = forms.CharField(
        label='Местоположение',
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Город или регион'}),
    )
    employment_type = forms.ChoiceField(
        label='Тип занятости',
        choices=[('', '---------')] + list(JobVacancy.EMPLOYMENT_TYPE_CHOICES),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    experience = forms.ChoiceField(
        label='Опыт работы',
        choices=[('', '---------')] + list(JobVacancy.EXPERIENCE_CHOICES),
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
    )
    remote = forms.BooleanField(
        label='Удаленная работа',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'}),
    ) 