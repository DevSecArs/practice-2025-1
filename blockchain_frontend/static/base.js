function adjustFooterPosition() {
    const footer = document.getElementById('footer');
    const bodyHeight = document.body.scrollHeight;
    const windowHeight = window.innerHeight;
    const currentPath = window.location.pathname;

    if (bodyHeight <= windowHeight && currentPath !== '/user') {
        footer.classList.add('absolute');
        footer.classList.remove('relative');
    } else {
        footer.classList.add('relative');
        footer.classList.remove('absolute');
    }
}

// Вызываем функцию при загрузке страницы и изменении размеров окна
document.addEventListener('DOMContentLoaded', adjustFooterPosition);
window.addEventListener('resize', adjustFooterPosition);