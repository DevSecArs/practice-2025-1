function toggleTheme() {
    const body = document.body;
    const navbar = document.getElementById('navbar');
    body.classList.toggle('dark-theme');
    if (body.classList.contains('dark-theme')) {
        navbar.classList.remove('navbar-light', 'bg-light');
        navbar.classList.add('navbar-dark', 'bg-dark');
    } else {
        navbar.classList.remove('navbar-dark', 'bg-dark');
        navbar.classList.add('navbar-light', 'bg-light');
    }
    const theme = body.classList.contains('dark-theme') ? 'dark' : 'light';
    localStorage.setItem('theme', theme);

    const table = document.querySelector('#transactions-container table');
    if (table) {
        table.classList.toggle('table-dark');
    }
}

document.addEventListener('DOMContentLoaded', () => {
    const savedTheme = localStorage.getItem('theme');
    const body = document.body;
    const navbar = document.getElementById('navbar');
    if (savedTheme === 'dark') {
        body.classList.add('dark-theme');
        navbar.classList.remove('navbar-light', 'bg-light');
        navbar.classList.add('navbar-dark', 'bg-dark');
    }
});
