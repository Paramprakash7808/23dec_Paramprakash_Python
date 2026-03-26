/* WriteSphere – Main JavaScript */

document.addEventListener('DOMContentLoaded', function () {

    // Auto-dismiss alerts after 5 seconds
    document.querySelectorAll('.alert.alert-dismissible').forEach(function (alert) {
        setTimeout(function () {
            const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
            bsAlert.close();
        }, 5000);
    });

    // Navbar scroll effect
    const navbar = document.getElementById('mainNavbar');
    if (navbar) {
        window.addEventListener('scroll', function () {
            if (window.scrollY > 50) {
                navbar.classList.add('scrolled');
            } else {
                navbar.classList.remove('scrolled');
            }
        });
    }

    // Confirm delete on any form with data-confirm
    document.querySelectorAll('[data-confirm]').forEach(function (el) {
        el.addEventListener('click', function (e) {
            if (!confirm(this.dataset.confirm)) {
                e.preventDefault();
            }
        });
    });

    // Back to top button
    const backToTop = document.createElement('button');
    backToTop.innerHTML = '<i class="bi bi-arrow-up"></i>';
    backToTop.className = 'btn btn-primary btn-sm back-to-top';
    backToTop.style.cssText = 'position:fixed;bottom:30px;right:30px;display:none;z-index:999;border-radius:50%;width:42px;height:42px;padding:0;';
    document.body.appendChild(backToTop);

    window.addEventListener('scroll', function () {
        backToTop.style.display = window.scrollY > 300 ? 'flex' : 'none';
        backToTop.style.alignItems = 'center';
        backToTop.style.justifyContent = 'center';
    });
    backToTop.addEventListener('click', function () {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });

    // Initialize Bootstrap tooltips
    document.querySelectorAll('[data-bs-toggle="tooltip"]').forEach(function (el) {
        new bootstrap.Tooltip(el);
    });

    // Character counter for textareas
    document.querySelectorAll('textarea[maxlength]').forEach(function (ta) {
        const counter = document.createElement('div');
        counter.className = 'form-text text-end';
        counter.textContent = `0 / ${ta.maxLength}`;
        ta.parentNode.appendChild(counter);
        ta.addEventListener('input', function () {
            counter.textContent = `${this.value.length} / ${this.maxLength}`;
        });
    });

});
