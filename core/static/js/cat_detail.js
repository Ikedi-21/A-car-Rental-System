// Car detail page — thumbnail swap + live price total.
// Split into its own file rather than main.js because this is
// page-specific logic, not something every page needs to load.

document.addEventListener('DOMContentLoaded', function () {

    // --- Thumbnail gallery ---
    // Simple swap-the-src approach. Doesn't need a carousel library
    // for four images.
    const mainImage = document.getElementById('mainCarImage');
    document.querySelectorAll('.dw-thumb').forEach(function (thumb) {
        thumb.addEventListener('click', function () {
            mainImage.src = thumb.dataset.full;
            document.querySelectorAll('.dw-thumb').forEach(t => t.classList.remove('active'));
            thumb.classList.add('active');
        });
    });

    // --- Booking price calculator ---
    const pickupInput = document.getElementById('pickupDate');
    const returnInput = document.getElementById('returnDate');
    const dayCountEl = document.getElementById('dayCount');
    const totalPriceEl = document.getElementById('totalPrice');
    const bookBtn = document.querySelector('[data-price-per-day]');

    if (!pickupInput || !bookBtn) return; // guard, in case markup changes later

    const pricePerDay = parseFloat(bookBtn.dataset.pricePerDay);

    const today = new Date().toISOString().split('T')[0];
    pickupInput.min = today;

    function recalcTotal() {
        if (!pickupInput.value || !returnInput.value) return;

        const pickup = new Date(pickupInput.value);
        const returnDate = new Date(returnInput.value);
        const diffTime = returnDate - pickup;
        const days = Math.round(diffTime / (1000 * 60 * 60 * 24));

        // Ignore nonsense ranges (return before pickup) rather than
        // showing a negative total, which would just look like a bug
        if (days <= 0) {
            dayCountEl.textContent = '0';
            totalPriceEl.textContent = '$0';
            return;
        }

        dayCountEl.textContent = days;
        totalPriceEl.textContent = '$' + (days * pricePerDay).toFixed(2);
    }

    pickupInput.addEventListener('change', function () {
        returnInput.min = pickupInput.value;
        if (returnInput.value && returnInput.value < pickupInput.value) {
            returnInput.value = '';
        }
        recalcTotal();
    });

    returnInput.addEventListener('change', recalcTotal);
});