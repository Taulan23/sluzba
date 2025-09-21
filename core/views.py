from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView, TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.db.models import Q
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import Article, ArticleCategory, News, Page, ContactMessage, FAQ, Tag
from .forms import ContactForm
from jobs.models import JobVacancy, Category as JobCategory

class HomeView(TemplateView):
    """Представление главной страницы"""
    template_name = 'core/home.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['latest_news'] = News.objects.filter(is_published=True)[:5]
        context['latest_articles'] = Article.objects.filter(is_published=True)[:3]
        context['latest_vacancies'] = JobVacancy.objects.filter(status='open')[:6]
        context['job_categories'] = JobCategory.objects.all()[:8]
        return context


class ArticleListView(ListView):
    """Представление списка статей"""
    model = Article
    template_name = 'core/article_list.html'
    context_object_name = 'articles'
    paginate_by = 6
    
    def get_queryset(self):
        queryset = Article.objects.filter(is_published=True)
        
        # Фильтрация по категории
        category_slug = self.kwargs.get('slug')
        if category_slug:
            category = get_object_or_404(ArticleCategory, slug=category_slug)
            queryset = queryset.filter(category=category)
        
        # Фильтрация по тегу
        tag_slug = self.kwargs.get('tag_slug')
        if tag_slug:
            tag = get_object_or_404(Tag, slug=tag_slug)
            queryset = queryset.filter(tags=tag)
        
        # Поиск
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(
                Q(title__icontains=q) | Q(content__icontains=q)
            )
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = ArticleCategory.objects.all()
        context['tags'] = Tag.objects.all()
        
        # Добавляем информацию о текущей категории
        category_slug = self.kwargs.get('slug')
        if category_slug:
            context['current_category'] = get_object_or_404(ArticleCategory, slug=category_slug)
        
        # Добавляем информацию о текущем теге
        tag_slug = self.kwargs.get('tag_slug')
        if tag_slug:
            context['current_tag'] = get_object_or_404(Tag, slug=tag_slug)
        
        return context


class ArticleDetailView(DetailView):
    """Представление отдельной статьи"""
    model = Article
    template_name = 'core/article_detail.html'
    context_object_name = 'article'
    
    def get_object(self):
        article = super().get_object()
        if article.is_published or self.request.user.is_staff:
            # Увеличиваем счетчик просмотров
            article.views += 1
            article.save()
            return article
        return get_object_or_404(Article, slug=self.kwargs['slug'], is_published=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        article = self.object
        # Добавляем связанные статьи из той же категории
        context['related_articles'] = Article.objects.filter(
            category=article.category, 
            is_published=True
        ).exclude(id=article.id)[:3]
        return context


class NewsListView(ListView):
    """Представление списка новостей"""
    model = News
    template_name = 'core/news_list.html'
    context_object_name = 'news_list'
    paginate_by = 6
    
    def get_queryset(self):
        queryset = News.objects.filter(is_published=True)
        
        # Поиск
        q = self.request.GET.get('q')
        if q:
            queryset = queryset.filter(
                Q(title__icontains=q) | Q(content__icontains=q)
            )
        
        return queryset


class NewsDetailView(DetailView):
    """Представление отдельной новости"""
    model = News
    template_name = 'core/news_detail.html'
    context_object_name = 'news'
    
    def get_object(self):
        news = super().get_object()
        if news.is_published or self.request.user.is_staff:
            # Увеличиваем счетчик просмотров
            news.views += 1
            news.save()
            return news
        return get_object_or_404(News, slug=self.kwargs['slug'], is_published=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        news_item = self.object
        # Показываем похожие новости вместо просто последних новостей
        context['similar_news'] = News.objects.filter(
            is_published=True
        ).exclude(id=news_item.id).order_by('-created_at')[:4]
        return context


class PageDetailView(DetailView):
    """Представление статической страницы"""
    model = Page
    template_name = 'core/page.html'
    context_object_name = 'page'
    
    def get_object(self):
        page = get_object_or_404(Page, slug=self.kwargs['slug'])
        if page.is_published or self.request.user.is_staff:
            return page
        return get_object_or_404(Page, slug=self.kwargs['slug'], is_published=True)


class ContactView(CreateView):
    """Представление контактной формы"""
    model = ContactMessage
    form_class = ContactForm
    template_name = 'core/contact.html'
    success_url = reverse_lazy('core:contact_success')
    
    def form_valid(self, form):
        messages.success(self.request, 'Ваше сообщение успешно отправлено!')
        return super().form_valid(form)


class ContactSuccessView(TemplateView):
    """Представление успешной отправки контактной формы"""
    template_name = 'core/contact_success.html'


class FAQView(ListView):
    """Представление FAQ"""
    model = FAQ
    template_name = 'core/faq.html'
    context_object_name = 'faqs'
    
    def get_queryset(self):
        return FAQ.objects.filter(is_published=True)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Группируем FAQ по категориям
        faqs = self.get_queryset()
        grouped_faqs = {}
        
        for faq in faqs:
            category = faq.category or 'Общие вопросы'
            if category not in grouped_faqs:
                grouped_faqs[category] = []
            grouped_faqs[category].append(faq)
        
        context['grouped_faqs'] = grouped_faqs
        return context


class SearchView(TemplateView):
    """Представление для поиска"""
    template_name = 'core/search_results.html'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        q = self.request.GET.get('q', '')
        
        if q:
            # Поиск по вакансиям
            vacancies = JobVacancy.objects.filter(
                Q(title__icontains=q) | 
                Q(description__icontains=q) |
                Q(requirements__icontains=q),
                status='open'
            )
            
            # Поиск по статьям
            articles = Article.objects.filter(
                Q(title__icontains=q) | 
                Q(content__icontains=q),
                is_published=True
            )
            
            # Поиск по новостям
            news = News.objects.filter(
                Q(title__icontains=q) | 
                Q(content__icontains=q),
                is_published=True
            )
            
            context['vacancies'] = vacancies[:5]
            context['articles'] = articles[:5]
            context['news'] = news[:5]
            context['query'] = q
            context['total_results'] = vacancies.count() + articles.count() + news.count()
        else:
            context['total_results'] = 0
        
        return context


def handler404(request, exception=None):
    """Обработчик ошибки 404"""
    return render(request, '404.html', status=404)
