// THIS FOR CREATE EVENT AND EDIT EVENT TEMPLATES
document.addEventListener('DOMContentLoaded', function () {
    const freeCheckbox = document.getElementById('free-checkbox');
    const priceInput = document.getElementById('price-input');
    const priceField = document.getElementById('price-field');
    const isOnlineCheckbox = document.getElementById('id_is_online');
    const locationFields = document.getElementById('location-fields');
    const requiredFields = [
        'id_venue_name',
        'id_address_line_1',
        'id_town_city',
        'id_postcode',
    ];

    function togglePriceField() {
        if (freeCheckbox && priceInput && priceField) {
            priceField.style.display = freeCheckbox.checked ? 'none' : 'block';
            priceInput.disabled = freeCheckbox.checked;
        }
    }

    function toggleLocationFields() {
        if (isOnlineCheckbox && locationFields) {
            locationFields.style.display = isOnlineCheckbox.checked ? 'none' : 'block';
            requiredFields.forEach(fieldId => {
                const field = document.getElementById(fieldId);
                if (field) {
                    field.required = !isOnlineCheckbox.checked;
                    field.disabled = isOnlineCheckbox.checked;
                }
            });
        }
    }

    // Initial toggle on page load
    togglePriceField();
    toggleLocationFields();

    // Add event listeners
    if (freeCheckbox) freeCheckbox.addEventListener('change', togglePriceField);
    if (isOnlineCheckbox) isOnlineCheckbox.addEventListener('change', toggleLocationFields);
});