document.addEventListener('DOMContentLoaded', () => {
    const menuItems = document.querySelectorAll('.menu li a');
    menuItems.forEach(item => {
        item.addEventListener('click', () => {
            menuItems.forEach(link => link.classList.remove('active'));
            item.classList.add('active');
        });
    });
});
