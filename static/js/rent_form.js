document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('rent-form');
    const startDateInput = document.getElementById('start_date');
    const dateError = document.getElementById('date-error');

    form.addEventListener('submit', function(event) {
        const selectedDate = new Date(startDateInput.value);
        const currentDate = new Date();

        currentDate.setHours(0, 0, 0, 0);

        if (selectedDate < currentDate) {
            event.preventDefault();
            dateError.style.display = 'block';
        } else {
            dateError.style.display = 'none';
        }
    });
});
