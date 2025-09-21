from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView, UpdateView, DetailView, ListView, TemplateView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.urls import reverse_lazy
from django.contrib import messages
from .models import JobSeekerProfile, EmployerProfile
from .forms import JobSeekerProfileForm, EmployerProfileForm, UserRegistrationForm
from jobs.models import JobApplication, JobVacancy

class UserRegistrationView(CreateView):
    """Представление для регистрации пользователя"""
    template_name = 'users/registration.html'
    form_class = UserRegistrationForm
    success_url = reverse_lazy('users:registration_success')
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        
        # Определяем тип пользователя и перенаправляем на соответствующую страницу создания профиля
        user_type = form.cleaned_data.get('user_type')
        
        if user_type == 'job_seeker':
            messages.success(self.request, 'Регистрация успешна! Пожалуйста, заполните профиль соискателя.')
            return redirect('users:job_seeker_profile_create')
        else:  # employer
            messages.success(self.request, 'Регистрация успешна! Пожалуйста, заполните профиль работодателя.')
            return redirect('users:employer_profile_create')
        
        return super().form_valid(form)


class RegistrationSuccessView(TemplateView):
    """Представление успешной регистрации"""
    template_name = 'users/registration_success.html'


class CustomLoginView(LoginView):
    """Кастомное представление входа"""
    template_name = 'users/login.html'
    redirect_authenticated_user = True
    
    def form_valid(self, form):
        messages.success(self.request, 'Вы успешно вошли в систему!')
        return super().form_valid(form)
    
    def get_success_url(self):
        return reverse_lazy('core:home')


class CustomLogoutView(LogoutView):
    """Кастомное представление выхода"""
    next_page = reverse_lazy('core:home')
    
    def dispatch(self, request, *args, **kwargs):
        messages.success(request, 'Вы успешно вышли из системы!')
        return super().dispatch(request, *args, **kwargs)


class JobSeekerProfileCreateView(LoginRequiredMixin, CreateView):
    """Представление создания профиля соискателя"""
    model = JobSeekerProfile
    form_class = JobSeekerProfileForm
    template_name = 'users/job_seeker_profile_form.html'
    success_url = reverse_lazy('core:home')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Профиль соискателя успешно создан!')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создание профиля соискателя'
        return context


class JobSeekerProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Представление редактирования профиля соискателя"""
    model = JobSeekerProfile
    form_class = JobSeekerProfileForm
    template_name = 'users/job_seeker_profile_form.html'
    
    def test_func(self):
        profile = self.get_object()
        return profile.user == self.request.user or self.request.user.is_staff
    
    def form_valid(self, form):
        messages.success(self.request, 'Профиль соискателя успешно обновлен!')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование профиля соискателя'
        return context


class JobSeekerProfileDetailView(DetailView):
    """Представление просмотра профиля соискателя"""
    model = JobSeekerProfile
    template_name = 'users/job_seeker_profile.html'
    context_object_name = 'profile'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Если пользователь просматривает свой профиль, показываем его заявки
        if self.request.user.is_authenticated and self.object.user == self.request.user:
            context['applications'] = JobApplication.objects.filter(job_seeker=self.object)[:5]
            context['is_owner'] = True
        else:
            context['is_owner'] = False
        
        return context


class EmployerProfileCreateView(LoginRequiredMixin, CreateView):
    """Представление создания профиля работодателя"""
    model = EmployerProfile
    form_class = EmployerProfileForm
    template_name = 'users/employer_profile_form.html'
    success_url = reverse_lazy('core:home')
    
    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, 'Профиль работодателя успешно создан!')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Создание профиля работодателя'
        return context


class EmployerProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    """Представление редактирования профиля работодателя"""
    model = EmployerProfile
    form_class = EmployerProfileForm
    template_name = 'users/employer_profile_form.html'
    
    def test_func(self):
        profile = self.get_object()
        return profile.user == self.request.user or self.request.user.is_staff
    
    def form_valid(self, form):
        messages.success(self.request, 'Профиль работодателя успешно обновлен!')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Редактирование профиля работодателя'
        return context


class EmployerProfileDetailView(DetailView):
    """Представление просмотра профиля работодателя"""
    model = EmployerProfile
    template_name = 'users/employer_profile.html'
    context_object_name = 'profile'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # Добавляем вакансии работодателя
        context['vacancies'] = JobVacancy.objects.filter(employer=self.object)[:5]
        
        # Если пользователь просматривает свой профиль
        if self.request.user.is_authenticated and self.object.user == self.request.user:
            context['is_owner'] = True
            # Добавляем заявки на вакансии этого работодателя
            context['applications'] = JobApplication.objects.filter(vacancy__employer=self.object)[:5]
        else:
            context['is_owner'] = False
        
        return context


class UserDashboardView(LoginRequiredMixin, TemplateView):
    """Представление панели управления пользователя"""
    template_name = 'users/dashboard.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        
        try:
            # Проверяем, является ли пользователь соискателем
            job_seeker_profile = JobSeekerProfile.objects.get(user=user)
            context['profile_type'] = 'job_seeker'
            context['profile'] = job_seeker_profile
            context['applications'] = JobApplication.objects.filter(job_seeker=job_seeker_profile)[:5]
        except JobSeekerProfile.DoesNotExist:
            try:
                # Проверяем, является ли пользователь работодателем
                employer_profile = EmployerProfile.objects.get(user=user)
                context['profile_type'] = 'employer'
                context['profile'] = employer_profile
                context['vacancies'] = JobVacancy.objects.filter(employer=employer_profile)[:5]
                context['applications'] = JobApplication.objects.filter(vacancy__employer=employer_profile)[:5]
            except EmployerProfile.DoesNotExist:
                # Профиль еще не создан
                context['profile_type'] = None
        
        return context
