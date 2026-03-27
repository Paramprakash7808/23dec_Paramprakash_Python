/*
 * Doctor Finder - JavaScript Validation
 * Practical 3: Create a Django project with JavaScript-enabled form validation.
 * Practical 10: JS used to validate email and phone number in registration form.
 */

"use strict";

// ── Practical 10: Real-time email validation ──────────────────
const emailField = document.getElementById('id_email');
if (emailField) {
    emailField.addEventListener('input', function () {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        const errorEl = document.getElementById('email_error');
        if (!emailRegex.test(this.value.trim())) {
            this.classList.add('is-invalid');
            if (errorEl) errorEl.textContent = 'Please enter a valid email address.';
        } else {
            this.classList.remove('is-invalid');
            this.classList.add('is-valid');
            if (errorEl) errorEl.textContent = '';
        }
    });
}

// ── Practical 10: Real-time phone number validation ───────────
const phoneField = document.getElementById('id_phone');
if (phoneField) {
    phoneField.addEventListener('input', function () {
        const phoneRegex = /^[6-9]\d{9}$/;
        const errorEl = document.getElementById('phone_error');
        if (!phoneRegex.test(this.value.trim())) {
            this.classList.add('is-invalid');
            if (errorEl) errorEl.textContent = 'Enter a valid 10-digit Indian mobile number starting with 6-9.';
        } else {
            this.classList.remove('is-invalid');
            this.classList.add('is-valid');
            if (errorEl) errorEl.textContent = '';
        }
    });
}

// ── Practical 3: Password match validation ────────────────────
const password2 = document.getElementById('id_password2');
if (password2) {
    password2.addEventListener('input', function () {
        const pass1 = document.getElementById('id_password1');
        const errorEl = document.getElementById('password2_error');
        if (pass1 && this.value !== pass1.value) {
            this.classList.add('is-invalid');
            if (errorEl) errorEl.textContent = 'Passwords do not match.';
        } else {
            this.classList.remove('is-invalid');
            this.classList.add('is-valid');
            if (errorEl) errorEl.textContent = '';
        }
    });
}

// ── Practical 3: Dismiss alerts after 4 seconds ───────────────
document.querySelectorAll('.alert.alert-dismissible').forEach(function (alert) {
    setTimeout(function () {
        const bsAlert = bootstrap.Alert.getOrCreateInstance(alert);
        if (bsAlert) bsAlert.close();
    }, 4000);
});
