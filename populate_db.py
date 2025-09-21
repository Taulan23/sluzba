import os
import django
import random
import lorem
from datetime import datetime, timedelta

# Настройка окружения Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'employment_project.settings')
django.setup()

from django.contrib.auth.models import User
from django.utils.text import slugify
from django.db import transaction
from core.models import ArticleCategory, Article, News, Page, FAQ
from jobs.models import Category, Skill, JobLocation, JobVacancy
from users.models import JobSeekerProfile, EmployerProfile

# Функция для создания тестовых данных
@transaction.atomic
def populate():
    print("Начинаем заполнение базы данных...")
    
    # Создаем категории статей
    article_categories_data = [
        {
            'name': 'Карьера',
            'description': 'Советы по построению карьеры и профессиональному развитию'
        },
        {
            'name': 'Собеседования',
            'description': 'Как подготовиться к собеседованию и успешно его пройти'
        },
        {
            'name': 'Резюме',
            'description': 'Советы по составлению эффективного резюме'
        },
        {
            'name': 'Рынок труда',
            'description': 'Анализ тенденций рынка труда и востребованных профессий'
        }
    ]
    
    print("Создаем категории статей...")
    article_categories = []
    for cat_data in article_categories_data:
        cat, created = ArticleCategory.objects.get_or_create(
            name=cat_data['name'],
            defaults={
                'description': cat_data['description'],
                'slug': slugify(cat_data['name']) + "-" + str(random.randint(1000, 9999))
            }
        )
        if created:
            print(f"  Создана категория статей: {cat.name}")
        else:
            print(f"  Категория статей '{cat.name}' уже существует.")
        article_categories.append(cat)
    
    # Создаем категории вакансий
    job_categories = [
        {
            'name': 'IT и разработка',
            'description': 'Вакансии в сфере информационных технологий и разработки ПО',
            'icon': 'fa-laptop-code'
        },
        {
            'name': 'Маркетинг',
            'description': 'Вакансии в сфере маркетинга, рекламы и PR',
            'icon': 'fa-chart-line'
        },
        {
            'name': 'Продажи',
            'description': 'Вакансии в сфере продаж и работы с клиентами',
            'icon': 'fa-handshake'
        },
        {
            'name': 'Финансы',
            'description': 'Вакансии в сфере финансов, бухгалтерии и банковского дела',
            'icon': 'fa-money-bill'
        },
        {
            'name': 'Администрирование',
            'description': 'Вакансии в сфере административной работы и офис-менеджмента',
            'icon': 'fa-tasks'
        },
        {
            'name': 'Образование',
            'description': 'Вакансии в сфере образования и науки',
            'icon': 'fa-graduation-cap'
        }
    ]
    
    print("Создаем категории вакансий...")
    for cat_data in job_categories:
        # Проверяем, существует ли категория
        try:
            Category.objects.get(name=cat_data['name'])
            print(f"  Категория вакансий '{cat_data['name']}' уже существует.")
        except Category.DoesNotExist:
            # Если категория не существует, создаем новую
            cat = Category(
                name=cat_data['name'],
                description=cat_data['description'],
                icon=cat_data['icon'],
                slug=slugify(cat_data['name']) + "-" + str(random.randint(1000, 9999))
            )
            cat.save()
            print(f"  Создана категория вакансий: {cat.name}")
    
    # Создаем навыки
    skills_list = [
        'Python', 'JavaScript', 'Java', 'C++', 'C#', 'PHP', 'Ruby',
        'HTML/CSS', 'SQL', 'Git', 'Docker', 'Kubernetes', 'React',
        'Angular', 'Vue.js', 'Django', 'Flask', 'Spring', 'Laravel',
        'Продажи', 'Маркетинг', 'SEO', 'SMM', 'Контекстная реклама',
        'Ведение переговоров', 'Работа с клиентами', 'Презентации',
        'MS Office', '1С', 'Бухгалтерия', 'Финансовый анализ',
        'Управление проектами', 'Agile', 'Scrum', 'Lean'
    ]
    
    print("Создаем навыки...")
    for skill_name in skills_list:
        # Проверяем, существует ли навык
        try:
            Skill.objects.get(name=skill_name)
            print(f"  Навык '{skill_name}' уже существует.")
        except Skill.DoesNotExist:
            # Если навык не существует, создаем новый
            skill = Skill(
                name=skill_name,
                slug=slugify(skill_name) + "-" + str(random.randint(1000, 9999))
            )
            skill.save()
            print(f"  Создан навык: {skill.name}")
    
    # Создаем местоположения
    locations = [
        {'city': 'Москва', 'region': 'Москва', 'address': 'ул. Тверская, 1'},
        {'city': 'Санкт-Петербург', 'region': 'Ленинградская область', 'address': 'Невский проспект, 1'},
        {'city': 'Екатеринбург', 'region': 'Свердловская область', 'address': 'ул. Ленина, 1'},
        {'city': 'Новосибирск', 'region': 'Новосибирская область', 'address': 'Красный проспект, 1'},
        {'city': 'Казань', 'region': 'Республика Татарстан', 'address': 'ул. Баумана, 1'}
    ]
    
    print("Создаем местоположения...")
    for loc_data in locations:
        # Проверяем, существует ли местоположение
        try:
            JobLocation.objects.get(
                city=loc_data['city'],
                region=loc_data['region'],
                address=loc_data['address']
            )
            print(f"  Местоположение '{loc_data['city']}, {loc_data['region']}' уже существует.")
        except JobLocation.DoesNotExist:
            # Если местоположение не существует, создаем новое
            location = JobLocation(
                city=loc_data['city'],
                region=loc_data['region'],
                address=loc_data['address']
            )
            location.save()
            print(f"  Создано местоположение: {location.city}, {location.region}")
    
    # Создаем работодателей и вакансии
    create_employers_and_vacancies()
    
    # Создаем статьи и новости
    create_articles_and_news(article_categories)
    
    # Создаем статические страницы
    pages = [
        {
            'title': 'О нас',
            'content': '''
            <h2>О нашей службе занятости</h2>
            <p>Мы являемся современной службой занятости, которая помогает соискателям найти работу, а работодателям — подходящих сотрудников.</p>
            <p>Наша миссия — сделать процесс трудоустройства максимально простым, быстрым и эффективным для всех участников рынка труда.</p>
            <h3>Наши преимущества:</h3>
            <ul>
                <li>Большая база вакансий и резюме</li>
                <li>Удобные инструменты поиска работы и сотрудников</li>
                <li>Профессиональные консультации и поддержка</li>
                <li>Современные технологии и инновационный подход</li>
            </ul>
            ''',
            'is_published': True,
            'is_in_menu': True,
            'menu_order': 1
        },
        {
            'title': 'Услуги',
            'content': '''
            <h2>Услуги нашей службы занятости</h2>
            <div class="row">
                <div class="col-md-6">
                    <h3>Для соискателей:</h3>
                    <ul>
                        <li>Поиск вакансий по различным параметрам</li>
                        <li>Создание и редактирование резюме</li>
                        <li>Автоматические уведомления о новых вакансиях</li>
                        <li>Консультации по составлению резюме и подготовке к собеседованию</li>
                        <li>Информация о состоянии рынка труда</li>
                    </ul>
                </div>
                <div class="col-md-6">
                    <h3>Для работодателей:</h3>
                    <ul>
                        <li>Публикация вакансий</li>
                        <li>Поиск сотрудников по базе резюме</li>
                        <li>Проведение собеседований</li>
                        <li>Аналитика по рынку труда</li>
                        <li>Консультации по подбору персонала</li>
                    </ul>
                </div>
            </div>
            ''',
            'is_published': True,
            'is_in_menu': True,
            'menu_order': 2
        },
        {
            'title': 'Правила использования',
            'content': '''
            <h2>Правила использования сервиса</h2>
            <p>Пожалуйста, ознакомьтесь с правилами использования нашего сервиса.</p>
            <h3>Общие положения</h3>
            <p>Настоящие правила определяют условия использования сервиса и регулируют отношения между пользователями и администрацией сайта.</p>
            <h3>Регистрация</h3>
            <p>Для использования всех функций сервиса необходимо зарегистрироваться. При регистрации пользователь обязуется предоставить достоверную информацию о себе.</p>
            <h3>Правила размещения информации</h3>
            <p>Запрещается размещать информацию, которая нарушает законодательство РФ, содержит нецензурную лексику, оскорбления, дискриминацию по любому признаку.</p>
            <h3>Конфиденциальность</h3>
            <p>Мы гарантируем сохранность личных данных пользователей и обязуемся не передавать их третьим лицам без согласия пользователя.</p>
            ''',
            'is_published': True,
            'is_in_menu': False,
            'menu_order': 0
        }
    ]
    
    print("Создаем статические страницы...")
    for page_data in pages:
        # Проверяем, существует ли страница
        try:
            Page.objects.get(title=page_data['title'])
            print(f"  Страница '{page_data['title']}' уже существует.")
        except Page.DoesNotExist:
            # Если страница не существует, создаем новую
            page = Page(
                title=page_data['title'],
                slug=slugify(page_data['title']) + "-" + str(random.randint(1000, 9999)),
                content=page_data['content'],
                is_published=page_data['is_published'],
                is_in_menu=page_data['is_in_menu'],
                menu_order=page_data['menu_order']
            )
            page.save()
            print(f"  Создана страница: {page.title}")
    
    # Создаем FAQ
    faqs = [
        {
            'question': 'Как зарегистрироваться на сайте?',
            'answer': 'Для регистрации на сайте нажмите кнопку "Регистрация" в верхнем меню, заполните форму и следуйте инструкциям.',
            'category': 'Регистрация',
            'order': 1
        },
        {
            'question': 'Как разместить вакансию?',
            'answer': 'Для размещения вакансии необходимо зарегистрироваться как работодатель, перейти в личный кабинет и нажать кнопку "Создать вакансию".',
            'category': 'Работодателям',
            'order': 2
        },
        {
            'question': 'Как откликнуться на вакансию?',
            'answer': 'Для отклика на вакансию перейдите на страницу интересующей вас вакансии и нажмите кнопку "Откликнуться".',
            'category': 'Соискателям',
            'order': 3
        },
        {
            'question': 'Сколько стоят услуги сайта?',
            'answer': 'Базовые функции сайта, такие как поиск вакансий и размещение резюме, бесплатны. Некоторые дополнительные услуги могут быть платными.',
            'category': 'Общие вопросы',
            'order': 4
        },
        {
            'question': 'Как изменить пароль?',
            'answer': 'Для изменения пароля перейдите в личный кабинет, выберите раздел "Настройки" и следуйте инструкциям.',
            'category': 'Профиль',
            'order': 5
        }
    ]
    
    print("Создаем FAQ...")
    for faq_data in faqs:
        # Проверяем, существует ли FAQ
        try:
            FAQ.objects.get(question=faq_data['question'])
            print(f"  FAQ '{faq_data['question']}' уже существует.")
        except FAQ.DoesNotExist:
            # Если FAQ не существует, создаем новый
            faq = FAQ(
                question=faq_data['question'],
                answer=faq_data['answer'],
                category=faq_data['category'],
                order=faq_data['order'],
                is_published=True
            )
            faq.save()
            print(f"  Создан FAQ: {faq.question}")
    
    # Создаем администратора
    print("Создаем администратора...")
    try:
        admin_user = User.objects.get(username='admin')
        print("  Администратор уже существует.")
    except User.DoesNotExist:
        admin_user = User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='admin123',
            first_name='Админ',
            last_name='Админов'
        )
        print("  Создан администратор: admin (пароль: admin123)")
    
    print("Заполнение базы данных завершено!")

def create_employers_and_vacancies():
    """Создает тестовых работодателей и вакансии"""
    
    print("Создаем работодателей и вакансии...")
    
    # Список компаний
    companies = [
        {
            'username': 'techcorp',
            'email': 'hr@techcorp.ru',
            'password': 'password123',
            'company_name': 'ТехКорп',
            'company_description': 'Инновационная технологическая компания, специализирующаяся на разработке программного обеспечения и цифровых решений для бизнеса.'
        },
        {
            'username': 'megamarket',
            'email': 'job@megamarket.ru',
            'password': 'password123',
            'company_name': 'МегаМаркет',
            'company_description': 'Крупная розничная сеть магазинов с широким ассортиментом товаров для дома, продуктов питания и бытовой техники.'
        },
        {
            'username': 'financeplus',
            'email': 'career@financeplus.ru',
            'password': 'password123',
            'company_name': 'ФинансПлюс',
            'company_description': 'Финансовая компания, предоставляющая широкий спектр банковских услуг, инвестиционные продукты и консультации по финансовому планированию.'
        },
        {
            'username': 'educentr',
            'email': 'hr@educentr.ru',
            'password': 'password123',
            'company_name': 'ОбразованиеЦентр',
            'company_description': 'Образовательный центр, предлагающий курсы повышения квалификации, профессиональную переподготовку и дополнительное образование для детей и взрослых.'
        },
        {
            'username': 'medservice',
            'email': 'vacancy@medservice.ru',
            'password': 'password123',
            'company_name': 'МедСервис',
            'company_description': 'Сеть медицинских клиник, предоставляющая широкий спектр медицинских услуг: от диагностики и профилактики до лечения и реабилитации.'
        }
    ]
    
    # Создаем работодателей
    employers = []
    for company_data in companies:
        # Проверяем, существует ли пользователь
        try:
            user = User.objects.get(username=company_data['username'])
            print(f"  Пользователь '{company_data['username']}' уже существует.")
            
            # Проверяем, существует ли профиль работодателя
            try:
                employer = EmployerProfile.objects.get(user=user)
                print(f"  Профиль работодателя для '{company_data['company_name']}' уже существует.")
                employers.append(employer)
            except EmployerProfile.DoesNotExist:
                # Если профиль не существует, создаем новый
                employer = EmployerProfile(
                    user=user,
                    company_name=company_data['company_name'],
                    company_description=company_data['company_description']
                )
                employer.save()
                employers.append(employer)
                print(f"  Создан профиль работодателя: {employer.company_name}")
                
        except User.DoesNotExist:
            # Если пользователь не существует, создаем нового
            user = User.objects.create_user(
                username=company_data['username'],
                email=company_data['email'],
                password=company_data['password'],
                first_name=company_data['company_name'][:30],
                last_name='HR'
            )
            
            employer = EmployerProfile(
                user=user,
                company_name=company_data['company_name'],
                company_description=company_data['company_description']
            )
            employer.save()
            employers.append(employer)
            print(f"  Создан работодатель: {employer.company_name}")
    
    # Категории вакансий
    categories = Category.objects.all()
    
    # Навыки
    skills = Skill.objects.all()
    
    # Местоположения
    locations = JobLocation.objects.all()
    
    # Варианты занятости
    employment_types = [
        'full_time', 'part_time', 'contract', 'internship', 'temporary'
    ]
    
    # Требуемый опыт
    experience_levels = [
        'no_experience', 'less_than_1', 'from_1_to_3', 'from_3_to_5', 'more_than_5'
    ]
    
    # Создаем вакансии для каждого работодателя
    for employer in employers:
        # От 3 до 6 вакансий для каждого работодателя
        num_vacancies = random.randint(3, 6)
        
        # Примеры вакансий для разных категорий
        it_positions = ['Python-разработчик', 'Frontend-разработчик', 'DevOps-инженер', 'Data Scientist', 'QA-специалист', 'Android-разработчик']
        marketing_positions = ['SMM-менеджер', 'Маркетолог-аналитик', 'Контент-менеджер', 'PR-менеджер', 'Бренд-менеджер']
        sales_positions = ['Менеджер по продажам', 'Торговый представитель', 'Руководитель отдела продаж', 'Специалист по работе с клиентами']
        finance_positions = ['Бухгалтер', 'Финансовый аналитик', 'Кредитный специалист', 'Финансовый контролер']
        admin_positions = ['Офис-менеджер', 'Администратор', 'Секретарь', 'Помощник руководителя']
        education_positions = ['Преподаватель', 'Методист', 'Репетитор', 'Тренер']
        
        positions_by_category = {
            'IT и разработка': it_positions,
            'Маркетинг': marketing_positions,
            'Продажи': sales_positions,
            'Финансы': finance_positions,
            'Администрирование': admin_positions,
            'Образование': education_positions
        }
        
        print(f"  Создаем вакансии для {employer.company_name}...")
        
        for i in range(num_vacancies):
            # Выбираем случайную категорию
            category = random.choice(categories)
            
            # Выбираем должность в соответствии с категорией
            if category.name in positions_by_category:
                position = random.choice(positions_by_category[category.name])
            else:
                position = f"Специалист ({category.name})"
            
            # Случайная зарплата
            salary_min = random.choice([None, 30000, 40000, 50000, 60000, 70000, 80000])
            
            if salary_min:
                salary_max = random.choice([None, salary_min + random.randint(10000, 50000)])
            else:
                salary_max = random.choice([None, 50000, 70000, 90000, 120000])
            
            # Случайное местоположение или удаленная работа
            is_remote = random.choice([True, False])
            location = None if is_remote else random.choice(locations)
            
            # Тип занятости и опыт
            employment_type = random.choice(employment_types)
            experience_required = random.choice(experience_levels)
            
            # Случайные навыки (от 3 до 6)
            vacancy_skills = random.sample(list(skills), random.randint(3, 6))
            
            # Создаем вакансию
            vacancy_title = f"{position} в {employer.company_name}"
            vacancy_slug = slugify(vacancy_title) + "-" + str(random.randint(1000, 9999))
            
            # Описание вакансии
            description = f"<h3>О компании:</h3><p>{employer.company_description}</p>"
            description += f"<h3>Обязанности:</h3><ul>"
            for _ in range(3, 6):
                description += f"<li>{str(lorem.sentence())}</li>"
            description += "</ul>"
            
            description += f"<h3>Требования:</h3><ul>"
            for skill in vacancy_skills:
                description += f"<li>{skill.name}</li>"
            description += "</ul>"
            
            description += f"<h3>Условия:</h3><ul>"
            for _ in range(3, 5):
                description += f"<li>{str(lorem.sentence())}</li>"
            description += "</ul>"
            
            try:
                # Проверяем, существует ли вакансия с таким slug
                JobVacancy.objects.get(slug=vacancy_slug)
                print(f"    Вакансия с slug '{vacancy_slug}' уже существует. Пропускаем.")
                continue
            except JobVacancy.DoesNotExist:
                # Создаем новую вакансию
                vacancy = JobVacancy(
                    title=vacancy_title,
                    slug=vacancy_slug,
                    employer=employer,
                    category=category,
                    description=description,
                    employment_type=employment_type,
                    experience_required=experience_required,
                    is_remote=is_remote,
                    location=location,
                    salary_min=salary_min,
                    salary_max=salary_max
                )
                vacancy.save()
                
                # Добавляем навыки
                vacancy.skills.set(vacancy_skills)
                
                print(f"    Создана вакансия: {vacancy.title}")

def create_articles_and_news(article_categories):
    """Создает тестовые статьи и новости"""
    print("Создаем статьи и новости...")

    if not article_categories:
        print("  Нет категорий статей для создания статей. Пропускаем создание статей.")
        article_categories = list(ArticleCategory.objects.all())
        if not article_categories:
             print("  Нет категорий статей в базе данных. Статьи не будут созданы.")
             # return # Если нет категорий, не можем создать статьи

    # Создаем статьи
    article_titles = [
        "Как успешно пройти собеседование",
        "Топ-10 востребованных навыков в 2024 году",
        "Секреты эффективного резюме",
        "Как сменить профессию: пошаговое руководство",
        "Удаленная работа: плюсы и минусы",
        "Как построить карьеру в IT",
        "Профессиональное выгорание: как распознать и предотвратить",
        "Личный бренд: зачем он нужен и как его создать",
        "Нетворкинг: искусство полезных знакомств",
        "Как вести переговоры о зарплате"
    ]

    print("  Создаем статьи...")
    for i in range(10): # Создадим 10 статей
        title = random.choice(article_titles) + f" (Часть {i+1})"
        slug = slugify(title) + "-" + str(random.randint(1000, 9999))
        content = "<p>" + str(lorem.paragraph()) + "</p>"
        content += "<p>" + str(lorem.paragraph()) + "</p>"
        content += "<h3>Подзаголовок</h3>"
        content += "<p>" + str(lorem.paragraph()) + "</p>"
        content += "<ul>"
        for _ in range(random.randint(3,5)):
            content += f"<li>{str(lorem.sentence())}</li>"
        content += "</ul>"

        # Проверяем, существует ли статья с таким slug
        if Article.objects.filter(slug=slug).exists():
            print(f"    Статья с slug '{slug}' уже существует. Пропускаем.")
            continue
        
        if article_categories: # Только если есть категории
            category = random.choice(article_categories)
            article = Article.objects.create(
                title=title,
                slug=slug,
                category=category,
                content=content,
                author=User.objects.get(username='admin'), # Предполагаем, что админ существует
                is_published=True,
                views=random.randint(10, 500)
            )
            print(f"    Создана статья: {article.title} в категории '{category.name}'")
        else:
            print(f"    Пропуск создания статьи '{title}', так как нет категорий.")

    # Создаем новости
    news_titles = [
        "Новый закон о труде вступает в силу",
        "Рынок труда: итоги квартала",
        "Конференция по управлению персоналом",
        "Вебинар: как найти работу мечты",
        "Исследование: самые высокооплачиваемые профессии",
        "Обновление нашего сервиса: новые функции",
        "Партнерство с ведущими компаниями",
        "Советы экспертов: как развивать карьеру",
        "Истории успеха наших пользователей",
        "Опрос: что важно для соискателей"
    ]

    print("  Создаем новости...")
    for i in range(10): # Создадим 10 новостей
        title = random.choice(news_titles) + f" (Новость {i+1})"
        slug = slugify(title) + "-" + str(random.randint(1000, 9999))
        content = "<p>" + str(lorem.paragraph()) + "</p>"
        content += "<p>" + str(lorem.paragraph()) + "</p>"
        
        # Проверяем, существует ли новость с таким slug
        if News.objects.filter(slug=slug).exists():
            print(f"    Новость с slug '{slug}' уже существует. Пропускаем.")
            continue

        news_item = News.objects.create(
            title=title,
            slug=slug,
            content=content,
            author=User.objects.get(username='admin'), # Предполагаем, что админ существует
            is_published=True,
            views=random.randint(50, 1000)
        )
        print(f"    Создана новость: {news_item.title}")

if __name__ == '__main__':
    populate() 