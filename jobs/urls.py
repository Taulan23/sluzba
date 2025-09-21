from django.urls import path
from . import views

app_name = 'jobs'

urlpatterns = [
    # Вакансии
    path('', views.JobVacancyListView.as_view(), name='vacancy_list'),
    path('category/<slug:slug>/', views.CategoryVacancyListView.as_view(), name='category'),
    
    # Создание и управление вакансиями (для работодателей)
    path('vacancy/create/', views.JobVacancyCreateView.as_view(), name='vacancy_create'),
    path('vacancy/<slug:slug>/update/', views.JobVacancyUpdateView.as_view(), name='vacancy_update'),
    path('vacancy/<slug:slug>/delete/', views.JobVacancyDeleteView.as_view(), name='vacancy_delete'),
    path('my-vacancies/', views.EmployerVacanciesView.as_view(), name='employer_vacancies'),
    
    # Детальная информация о вакансии (должна быть ПОСЛЕ специфических URL)
    path('vacancy/<slug:slug>/', views.JobVacancyDetailView.as_view(), name='vacancy_detail'),
    
    # Заявки на вакансии
    path('vacancy/<slug:vacancy_slug>/apply/', views.JobApplicationCreateView.as_view(), name='apply'),
    path('my-applications/', views.JobSeekerApplicationsView.as_view(), name='job_seeker_applications'),
    path('employer/applications/', views.EmployerApplicationsView.as_view(), name='employer_applications'),
] 