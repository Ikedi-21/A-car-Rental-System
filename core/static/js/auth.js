// Login/register pages. Currently light — the password show/hide toggle
// is already handled globally in main.js since it's used on multiple
// pages (login, register, change password). This file is here for
// anything auth-specific that comes up later, e.g. live password-match
// checking on register, so it's not all jammed into main.js.

document.addEventListener('DOMContentLoaded', function () {

    // Live-check that password confirmation matches password1 as the user
    // types, rather than making them submit the form to find out — small
    // thing but it's the difference between a form that feels responsive
    // and one that feels like it's fighting you
    const pw1 = document.querySelector('#id_password1');
    const pw2 = document.querySelector('#id_password2');

    if (!pw1 || !pw2) return; // not on the register page, nothing to do here

    function checkMatch() {
        if (pw2.value && pw1.value !== pw2.value) {
            pw2.style.borderColor = 'var(--dw-danger)';
        } else {
            pw2.style.borderColor = '';
        }
    }

    pw1.addEventListener('input', checkMatch);
    pw2.addEventListener('input', checkMatch);
});