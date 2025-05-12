function copyToClipboard(text) {
    // Создаем временный элемент textarea
    const textarea = document.createElement('textarea');
    textarea.value = text;
    textarea.style.position = 'fixed';
    textarea.style.opacity = '0';
    document.body.appendChild(textarea);
    
    // Пробуем оба метода копирования
    try {
        // Современный API
        if (navigator.clipboard) {
            navigator.clipboard.writeText(text).then(() => {
                showToast('Адрес скопирован в буфер обмена!');
            }).catch(() => {
                // Fallback для старых браузеров
                fallbackCopy(textarea);
            });
        } else {
            // Старый метод
            fallbackCopy(textarea);
        }
    } catch (err) {
        showToast('Не удалось скопировать адрес', true);
    } finally {
        // Удаляем временный элемент
        document.body.removeChild(textarea);
    }
}

function fallbackCopy(textarea) {
    textarea.select();
    try {
        const successful = document.execCommand('copy');
        if (successful) {
            showToast('Адрес скопирован в буфер обмена!');
        } else {
            throw new Error('Copy failed');
        }
    } catch (err) {
        showToast('Не удалось скопировать адрес', true);
    }
}

function showToast(message, isError = false) {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.style.backgroundColor = isError ? '#f44336' : '#4CAF50';
    
    toast.classList.add('show');
    
    setTimeout(() => {
        toast.classList.remove('show');
    }, 3000);
}