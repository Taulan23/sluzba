/**
 * Custom JavaScript for the Django Admin
 */

document.addEventListener('DOMContentLoaded', function() {
    // Проверка поддержки localStorage
    const storageAvailable = function(type) {
        let storage;
        try {
            storage = window[type];
            const x = '__storage_test__';
            storage.setItem(x, x);
            storage.removeItem(x);
            return true;
        } catch (e) {
            return false;
        }
    };

    // Инициализация темной темы
    const initDarkMode = function() {
        const toggle = document.getElementById('dark-mode-toggle');
        if (!toggle) return;

        // Проверяем сохраненное значение в localStorage, если оно доступно
        if (storageAvailable('localStorage')) {
            const darkMode = localStorage.getItem('adminDarkMode') === 'true';
            if (darkMode) {
                document.body.classList.add('dark-mode');
                toggle.checked = true;
            }
        }

        // Обработчик переключения темы
        toggle.addEventListener('change', function() {
            if (this.checked) {
                document.body.classList.add('dark-mode');
                if (storageAvailable('localStorage')) {
                    localStorage.setItem('adminDarkMode', 'true');
                }
            } else {
                document.body.classList.remove('dark-mode');
                if (storageAvailable('localStorage')) {
                    localStorage.setItem('adminDarkMode', 'false');
                }
            }
        });
    };

    // Создание переключателя темы в правом верхнем углу
    const createDarkModeToggle = function() {
        const userTools = document.getElementById('user-tools');
        if (!userTools) return;

        const themeToggleLabel = document.createElement('label');
        themeToggleLabel.className = 'theme-toggle';
        themeToggleLabel.title = 'Переключить темную тему';

        const themeToggleInput = document.createElement('input');
        themeToggleInput.type = 'checkbox';
        themeToggleInput.id = 'dark-mode-toggle';

        const themeToggleSpan = document.createElement('span');
        themeToggleSpan.className = 'theme-toggle__toggle';

        themeToggleLabel.appendChild(themeToggleInput);
        themeToggleLabel.appendChild(themeToggleSpan);

        // Добавляем переключатель после текстового содержимого
        userTools.appendChild(document.createTextNode(' '));
        userTools.appendChild(themeToggleLabel);

        // Инициализация
        initDarkMode();
    };

    // Улучшения для мобильной версии
    const enhanceMobileExperience = function() {
        if (window.innerWidth <= 767) {
            // Добавляем кнопку для мобильной навигации
            const header = document.getElementById('header');
            if (!header) return;

            const mobileMenuBtn = document.createElement('button');
            mobileMenuBtn.className = 'mobile-menu-btn';
            mobileMenuBtn.innerHTML = '<span></span><span></span><span></span>';
            mobileMenuBtn.setAttribute('aria-label', 'Меню навигации');
            
            header.insertBefore(mobileMenuBtn, header.firstChild);

            // Обработчик мобильного меню
            mobileMenuBtn.addEventListener('click', function() {
                const sidebar = document.getElementById('nav-sidebar');
                if (sidebar) {
                    sidebar.classList.toggle('nav-sidebar-mobile-active');
                    this.classList.toggle('active');
                }
            });
        }
    };

    // Улучшаем табличные списки моделей для лучшей читаемости на мобильных
    const enhanceModelLists = function() {
        const tables = document.querySelectorAll('#changelist-form .results, .dashboard table');
        tables.forEach(function(table) {
            table.classList.add('responsive-table');
            
            // Добавляем обработчик для строк таблицы
            const rows = table.querySelectorAll('tbody tr');
            rows.forEach(function(row) {
                row.addEventListener('click', function(e) {
                    // Если пользователь кликнул на чекбокс или ссылку, не делаем ничего
                    if (e.target.tagName === 'INPUT' || e.target.tagName === 'A' || e.target.tagName === 'TH') {
                        return;
                    }
                    
                    // Находим первую ссылку в строке и переходим по ней
                    const firstLink = this.querySelector('a');
                    if (firstLink && firstLink.href) {
                        window.location.href = firstLink.href;
                    }
                });
            });
        });
    };

    // Улучшение форм фильтрации для лучшей мобильной видимости
    const enhanceFilterForms = function() {
        const filterBtn = document.querySelector('.filter-button');
        if (filterBtn) {
            filterBtn.addEventListener('click', function() {
                const filters = document.getElementById('changelist-filter');
                if (filters) {
                    filters.classList.toggle('filters-visible');
                }
            });
        }
    };

    // Улучшение селекторов для ManyToMany полей
    const enhanceSelectors = function() {
        const selectors = document.querySelectorAll('.selector');
        selectors.forEach(function(selector) {
            // Улучшенный поиск для селекторов
            const availableSelect = selector.querySelector('.selector-available select');
            if (availableSelect) {
                const searchBox = document.createElement('input');
                searchBox.type = 'text';
                searchBox.className = 'selector-search';
                searchBox.placeholder = 'Поиск...';
                
                // Вставляем перед селектом
                availableSelect.parentNode.insertBefore(searchBox, availableSelect);
                
                // Обработчик поиска
                searchBox.addEventListener('input', function() {
                    const searchTerm = this.value.toLowerCase();
                    const options = availableSelect.querySelectorAll('option');
                    
                    options.forEach(function(option) {
                        const text = option.textContent.toLowerCase();
                        if (text.includes(searchTerm)) {
                            option.style.display = '';
                        } else {
                            option.style.display = 'none';
                        }
                    });
                });
            }
        });
    };

    // Красивые алерты для сообщений
    const enhanceMessages = function() {
        const messages = document.querySelectorAll('.messagelist li');
        messages.forEach(function(message) {
            // Добавляем иконку в зависимости от типа сообщения
            let icon = '';
            if (message.classList.contains('success')) {
                icon = '<i class="fas fa-check-circle"></i> ';
            } else if (message.classList.contains('warning')) {
                icon = '<i class="fas fa-exclamation-triangle"></i> ';
            } else if (message.classList.contains('error')) {
                icon = '<i class="fas fa-times-circle"></i> ';
            } else {
                icon = '<i class="fas fa-info-circle"></i> ';
            }
            
            message.innerHTML = icon + message.innerHTML;
            
            // Добавляем кнопку закрытия
            const closeBtn = document.createElement('button');
            closeBtn.className = 'message-close';
            closeBtn.innerHTML = '&times;';
            closeBtn.setAttribute('aria-label', 'Закрыть');
            
            message.appendChild(closeBtn);
            
            closeBtn.addEventListener('click', function() {
                message.style.opacity = '0';
                setTimeout(function() {
                    message.style.display = 'none';
                }, 300);
            });
        });
    };

    // Плавная автоматическая высота для текстовых полей
    const enhanceTextareas = function() {
        const textareas = document.querySelectorAll('textarea');
        textareas.forEach(function(textarea) {
            textarea.addEventListener('input', function() {
                this.style.height = 'auto';
                this.style.height = (this.scrollHeight) + 'px';
            });
            
            // Инициализируем начальную высоту
            textarea.dispatchEvent(new Event('input'));
        });
    };
    
    // Запускаем улучшения
    createDarkModeToggle();
    enhanceMobileExperience();
    enhanceModelLists();
    enhanceFilterForms();
    enhanceSelectors();
    enhanceMessages();
    enhanceTextareas();
}); 