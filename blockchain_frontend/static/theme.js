function toggleTheme() {
    const body = document.body;
    const navbar = document.getElementById('navbar');
    const footer = document.getElementById('footer');

    body.classList.toggle('dark-theme');
    if (body.classList.contains('dark-theme')) {
        navbar.classList.remove('navbar-light', 'bg-light', 'border-dark');
        footer.classList.remove('navbar-light', 'bg-light', 'border-dark');

        navbar.classList.add('navbar-dark', 'bg-dark', 'border-light');
        footer.classList.add('navbar-dark', 'bg-dark', 'border-light');
    } else {
        navbar.classList.remove('navbar-dark', 'bg-dark', 'border-light');
        footer.classList.remove('navbar-dark', 'bg-dark', 'border-light');

        navbar.classList.add('navbar-light', 'bg-light', 'border-dark');
        footer.classList.add('navbar-light', 'bg-light', 'border-dark');
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
    const footer = document.getElementById('footer');
    if (savedTheme === 'dark') {
        body.classList.add('dark-theme');
        navbar.classList.remove('navbar-light', 'bg-light', 'border-dark');
        footer.classList.remove('navbar-light', 'bg-light', 'border-dark');

        navbar.classList.add('navbar-dark', 'bg-dark', 'border-light');
        footer.classList.add('navbar-dark', 'bg-dark', 'border-light');
    }
});
