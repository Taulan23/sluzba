// Функция для переключения режима для слабовидящих
function toggleHighContrast() {
    document.body.classList.toggle('high-contrast');
    
    // Сохраняем выбор пользователя в localStorage
    if (document.body.classList.contains('high-contrast')) {
        localStorage.setItem('high-contrast', 'true');
    } else {
        localStorage.setItem('high-contrast', 'false');
    }
}

// Функция для переключения размера шрифта
function toggleLargeFont() {
    document.body.classList.toggle('large-font');
    
    // Сохраняем выбор пользователя в localStorage
    if (document.body.classList.contains('large-font')) {
        localStorage.setItem('large-font', 'true');
    } else {
        localStorage.setItem('large-font', 'false');
    }
}

// Проверяем настройки при загрузке страницы
document.addEventListener('DOMContentLoaded', function() {
    // Проверяем наличие сохраненных настроек для высокого контраста
    if (localStorage.getItem('high-contrast') === 'true') {
        document.body.classList.add('high-contrast');
    }
    
    // Проверяем наличие сохраненных настроек для увеличенного шрифта
    if (localStorage.getItem('large-font') === 'true') {
        document.body.classList.add('large-font');
    }
    
    // Добавляем обработчики событий для кнопок переключения режимов
    const contrastToggle = document.getElementById('contrast-toggle');
    const fontSizeToggle = document.getElementById('font-size-toggle');
    
    if (contrastToggle) {
        contrastToggle.addEventListener('click', toggleHighContrast);
    }
    
    if (fontSizeToggle) {
        fontSizeToggle.addEventListener('click', toggleLargeFont);
    }
}); 