// THIS SCRIPT IS FOR THE CREATE EVENT AND EDIT EVENT TEMPLATES

document.addEventListener('DOMContentLoaded', function () {
    /**
     * Get references to the DOM elements for toggling fields.
     */
    const freeCheckbox = document.getElementById('free-checkbox'); // Checkbox to indicate if the event is free
    const priceInput = document.getElementById('price-input'); // Input field for event price
    const priceField = document.getElementById('price-field'); // Container for the price input field
    const isOnlineCheckbox = document.getElementById('id_is_online'); // Checkbox to indicate if the event is online
    const locationFields = document.getElementById('location-fields'); // Container for location-specific fields
    const requiredFields = [ // Array of location-specific field IDs
        'id_venue_name',
        'id_address_line_1',
        'id_town_city',
        'id_postcode',
    ];

    /**
     * Toggles the visibility and enable/disable state of the price field based on the free checkbox.
     * If the event is marked as free, the price field is hidden and disabled.
     * If the event is not free, the price field is shown and enabled.
     */
    function togglePriceField() {
        if (freeCheckbox && priceInput && priceField) {
            priceField.style.display = freeCheckbox.checked ? 'none' : 'block'; // Hide or show the price field
            priceInput.disabled = freeCheckbox.checked; // Disable price input if event is free
        }
    }

    /**
     * Toggles the visibility and required/disabled state of location fields based on the isOnline checkbox.
     * If the event is marked as online, the location fields are hidden and disabled.
     * If the event is in-person, the location fields are shown and required.
     */
    function toggleLocationFields() {
        if (isOnlineCheckbox && locationFields) {
            locationFields.style.display = isOnlineCheckbox.checked ? 'none' : 'block'; // Hide or show location fields
            requiredFields.forEach(fieldId => {
                const field = document.getElementById(fieldId); // Get each location-specific field
                if (field) {
                    field.required = !isOnlineCheckbox.checked; // Make fields required if event is in-person
                    field.disabled = isOnlineCheckbox.checked; // Disable fields if event is online
                }
            });
        }
    }

    // ** Initial Toggle on Page Load **
    togglePriceField(); // Set the initial state of the price field
    toggleLocationFields(); // Set the initial state of the location fields

    // ** Add Event Listeners **
    if (freeCheckbox) freeCheckbox.addEventListener('change', togglePriceField); // Listen for changes on the free checkbox
    if (isOnlineCheckbox) isOnlineCheckbox.addEventListener('change', toggleLocationFields); // Listen for changes on the isOnline checkbox
});

/**
 * Toggles the user type between "Event User" and "Event Organiser" in the signup form.
 *
 * This function updates:
 * 1. The label displayed next to the switch input.
 * 2. The hidden input field's value, which is sent with the form submission.
 *
 * The function checks the state of the switch (`checked` or not) and updates:
 * - Label text to "Event Organiser" if checked, otherwise "Event User".
 * - Hidden input value to "event_organiser" if checked, otherwise "event_user".
 */
function toggleUserType() {
    const switchInput = document.getElementById('userTypeSwitch');
    const userTypeLabel = document.getElementById('userTypeLabel');
    const userTypeInput = document.getElementById('user_type_input');

    // Fetch the translated strings from the data attributes
    const eventUserText = switchInput.getAttribute('data-event-user');
    const eventOrganiserText = switchInput.getAttribute('data-event-organiser');

    if (switchInput.checked) {
        userTypeLabel.textContent = eventOrganiserText;
        userTypeInput.value = 'event_organiser';
    } else {
        userTypeLabel.textContent = eventUserText;
        userTypeInput.value = 'event_user';
    }
}
