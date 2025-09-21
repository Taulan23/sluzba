from django.urls import path
from . import views

app_name = 'core'

urlpatterns = [
    # Главная страница
    path('', views.HomeView.as_view(), name='home'),
    
    # Статьи
    path('articles/', views.ArticleListView.as_view(), name='article_list'),
    path('articles/category/<slug:slug>/', views.ArticleListView.as_view(), name='article_category'),
    path('articles/tag/<slug:tag_slug>/', views.ArticleListView.as_view(), name='article_tag'),
    path('articles/<slug:slug>/', views.ArticleDetailView.as_view(), name='article_detail'),
    
    # Новости
    path('news/', views.NewsListView.as_view(), name='news_list'),
    path('news/<slug:slug>/', views.NewsDetailView.as_view(), name='news_detail'),
    
    # Статические страницы
    path('page/<slug:slug>/', views.PageDetailView.as_view(), name='page'),
    
    # Контакты
    path('contact/', views.ContactView.as_view(), name='contact'),
    path('contact/success/', views.ContactSuccessView.as_view(), name='contact_success'),
    
    # FAQ
    path('faq/', views.FAQView.as_view(), name='faq'),
    
    # Поиск
    path('search/', views.SearchView.as_view(), name='search'),
] 