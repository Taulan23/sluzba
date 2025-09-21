from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # Регистрация и аутентификация
    path('register/', views.UserRegistrationView.as_view(), name='register'),
    path('register/success/', views.RegistrationSuccessView.as_view(), name='registration_success'),
    path('login/', views.CustomLoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    
    # Панель управления пользователя
    path('dashboard/', views.UserDashboardView.as_view(), name='dashboard'),
    
    # Профиль соискателя
    path('job-seeker/create/', views.JobSeekerProfileCreateView.as_view(), name='job_seeker_profile_create'),
    path('job-seeker/<slug:slug>/update/', views.JobSeekerProfileUpdateView.as_view(), name='job_seeker_profile_update'),
    path('job-seeker/<slug:slug>/', views.JobSeekerProfileDetailView.as_view(), name='job_seeker_profile'),
    
    # Профиль работодателя
    path('employer/create/', views.EmployerProfileCreateView.as_view(), name='employer_profile_create'),
    path('employer/<slug:slug>/update/', views.EmployerProfileUpdateView.as_view(), name='employer_profile_update'),
    path('employer/<slug:slug>/', views.EmployerProfileDetailView.as_view(), name='employer_profile'),
] 