// --- Home page: search bar date logic ---
// Without this, someone can pick a return date before their pickup date
// and the booking would be nonsensical by the time it hits the backend.
// Cheaper to stop it here than to bounce it back with a form error later.
(function () {
    const pickupInput = document.querySelector('input[name="pickup_date"]');
    const returnInput = document.querySelector('input[name="return_date"]');

    if (!pickupInput || !returnInput) return; // not on this page, bail out

    const today = new Date().toISOString().split('T')[0];
    pickupInput.min = today;

    pickupInput.addEventListener('change', function () {
        // return date can't be before whatever pickup date was just chosen
        returnInput.min = pickupInput.value;

        // if they'd already picked a return date that's now invalid, clear it
        // rather than silently letting a bad range through
        if (returnInput.value && returnInput.value < pickupInput.value) {
            returnInput.value = '';
        }
    });
})();