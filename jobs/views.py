from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.db.models import Q
from django.contrib import messages
from .models import JobVacancy, Category, Skill, JobLocation, JobApplication
from users.models import EmployerProfile, JobSeekerProfile
from .forms import JobVacancyForm, JobApplicationForm, JobSearchForm

class JobVacancyListView(ListView):
    """Представление списка вакансий"""
    model = JobVacancy
    template_name = 'jobs/vacancy_list.html'
    context_object_name = 'vacancies'
    paginate_by = 10
    
    def get_queryset(self):
        queryset = JobVacancy.objects.filter(status='open')
        
        # Фильтрация по форме поиска
        form = JobSearchForm(self.request.GET)
        if form.is_valid():
            # Поиск по ключевым словам
            keywords = form.cleaned_data.get('keywords')
            if keywords:
                queryset = queryset.filter(
                    Q(title__icontains=keywords) | 
                    Q(description__icontains=keywords) |
                    Q(requirements__icontains=keywords)
                )
            
            # Фильтрация по категории
            category = form.cleaned_data.get('category')
            if category:
                queryset = queryset.filter(category=category)
            
            # Фильтрация по местоположению
            location = form.cleaned_data.get('location')
            if location:
                queryset = queryset.filter(location__city__icontains=location)
            
            # Фильтрация по типу занятости
            employment_type = form.cleaned_data.get('employment_type')
            if employment_type:
                queryset = queryset.filter(employment_type=employment_type)
            
            # Фильтрация по опыту
            experience = form.cleaned_data.get('experience')
            if experience:
                queryset = queryset.filter(experience_required=experience)
            
            # Фильтрация по удаленной работе
            remote = form.cleaned_data.get('remote')
            if remote:
                queryset = queryset.filter(is_remote=True)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['search_form'] = JobSearchForm(self.request.GET)
        context['categories'] = Category.objects.all()
        return context


class CategoryVacancyListView(ListView):
    """Представление вакансий по категории"""
    model = JobVacancy
    template_name = 'jobs/category_vacancies.html'
    context_object_name = 'vacancies'
    paginate_by = 10
    
    def get_queryset(self):
        self.category = get_object_or_404(Category, slug=self.kwargs['slug'])
        return JobVacancy.objects.filter(category=self.category, status='open')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        context['categories'] = Category.objects.all()
        return context


class JobVacancyDetailView(DetailView):
    """Представление отдельной вакансии"""
    model = JobVacancy
    template_name = 'jobs/vacancy_detail.html'
    context_object_name = 'vacancy'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Добавляем похожие вакансии из той же категории
        vacancy = self.object
        context['similar_vacancies'] = JobVacancy.objects.filter(
            category=vacancy.category, 
            status='open'
        ).exclude(id=vacancy.id)[:4]
        
        # Добавляем форму заявки, если пользователь авторизован и является соискателем
        if self.request.user.is_authenticated:
            try:
                job_seeker = JobSeekerProfile.objects.get(user=self.request.user)
                # Проверяем, не подавал ли уже пользователь заявку на эту вакансию
                has_applied = JobApplication.objects.filter(job_seeker=job_seeker, vacancy=vacancy).exists()
                context['has_applied'] = has_applied
                
                if not has_applied:
                    context['application_form'] = JobApplicationForm()
            except JobSeekerProfile.DoesNotExist:
                pass
        
        return context


class JobVacancyCreateView(LoginRequiredMixin, CreateView):
    """Представление создания вакансии"""
    model = JobVacancy
    form_class = JobVacancyForm
    template_name = 'jobs/vacancy_form.html'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['employer'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        try:
            employer = EmployerProfile.objects.get(user=self.request.user)
            form.instance.employer = employer
            messages.success(self.request, 'Вакансия успешно создана!')
            return super().form_valid(form)
        except EmployerProfile.DoesNotExist:
            messages.error(self.request, 'Вы должны создать профиль работодателя перед публикацией вакансий.')
            return redirect('users:employer_profile_create')


class JobVacancyUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Представление редактирования вакансии"""
    model = JobVacancy
    form_class = JobVacancyForm
    template_name = 'jobs/vacancy_form.html'
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['employer'] = self.request.user
        return kwargs
    
    def test_func(self):
        vacancy = self.get_object()
        return vacancy.employer.user == self.request.user or self.request.user.is_staff
    
    def form_valid(self, form):
        messages.success(self.request, 'Вакансия успешно обновлена!')
        return super().form_valid(form)


class JobVacancyDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    """Представление удаления вакансии"""
    model = JobVacancy
    template_name = 'jobs/vacancy_confirm_delete.html'
    success_url = reverse_lazy('jobs:employer_vacancies')
    
    def test_func(self):
        vacancy = self.get_object()
        return vacancy.employer.user == self.request.user or self.request.user.is_staff
    
    def delete(self, request, *args, **kwargs):
        messages.success(self.request, 'Вакансия успешно удалена!')
        return super().delete(request, *args, **kwargs)


class EmployerVacanciesView(LoginRequiredMixin, ListView):
    """Представление списка вакансий работодателя"""
    model = JobVacancy
    template_name = 'jobs/employer_vacancies.html'
    context_object_name = 'vacancies'
    paginate_by = 10
    
    def get_queryset(self):
        try:
            employer = EmployerProfile.objects.get(user=self.request.user)
            return JobVacancy.objects.filter(employer=employer)
        except EmployerProfile.DoesNotExist:
            return JobVacancy.objects.none()


class JobApplicationCreateView(LoginRequiredMixin, CreateView):
    """Представление создания заявки на вакансию"""
    model = JobApplication
    form_class = JobApplicationForm
    template_name = 'jobs/application_form.html'
    
    def get_vacancy(self):
        return get_object_or_404(JobVacancy, slug=self.kwargs['vacancy_slug'])
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['vacancy'] = self.get_vacancy()
        return context
    
    def form_valid(self, form):
        try:
            job_seeker = JobSeekerProfile.objects.get(user=self.request.user)
            form.instance.job_seeker = job_seeker
            form.instance.vacancy = self.get_vacancy()
            
            # Проверяем, не подавал ли пользователь уже заявку на эту вакансию
            if JobApplication.objects.filter(job_seeker=job_seeker, vacancy=form.instance.vacancy).exists():
                messages.error(self.request, 'Вы уже подали заявку на эту вакансию.')
                return redirect('jobs:vacancy_detail', slug=form.instance.vacancy.slug)
            
            messages.success(self.request, 'Заявка успешно отправлена!')
            return super().form_valid(form)
        except JobSeekerProfile.DoesNotExist:
            messages.error(self.request, 'Вы должны создать профиль соискателя перед подачей заявок.')
            return redirect('users:job_seeker_profile_create')
    
    def get_success_url(self):
        return reverse_lazy('jobs:vacancy_detail', kwargs={'slug': self.get_vacancy().slug})


class JobSeekerApplicationsView(LoginRequiredMixin, ListView):
    """Представление списка заявок соискателя"""
    model = JobApplication
    template_name = 'jobs/job_seeker_applications.html'
    context_object_name = 'applications'
    paginate_by = 10
    
    def get_queryset(self):
        try:
            job_seeker = JobSeekerProfile.objects.get(user=self.request.user)
            return JobApplication.objects.filter(job_seeker=job_seeker)
        except JobSeekerProfile.DoesNotExist:
            return JobApplication.objects.none()


class EmployerApplicationsView(LoginRequiredMixin, ListView):
    """Представление списка заявок на вакансии работодателя"""
    model = JobApplication
    template_name = 'jobs/employer_applications.html'
    context_object_name = 'applications'
    paginate_by = 10
    
    def get_queryset(self):
        try:
            employer = EmployerProfile.objects.get(user=self.request.user)
            return JobApplication.objects.filter(vacancy__employer=employer)
        except EmployerProfile.DoesNotExist:
            return JobApplication.objects.none()
