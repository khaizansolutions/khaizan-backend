// Static file: products/static/admin/js/product_conditional_fields.js

(function($) {
    'use strict';

    $(document).ready(function() {
        console.log('Product conditional fields script loaded');

        // Function to toggle field visibility based on product type
        function toggleConditionalFields() {
            var productType = $('input[name="product_type"]:checked').val();
            console.log('Selected product type:', productType);

            // Hide all conditional sections first
            $('.rental-section').hide();
            $('.refurbished-section').hide();

            // Hide all conditional fields
            $('.rental-field').closest('.form-row').hide();
            $('.refurbished-field').closest('.form-row').hide();

            // Show relevant sections and fields based on product type
            if (productType === 'rental') {
                console.log('Showing rental fields');
                $('.rental-section').show();
                $('.rental-field').closest('.form-row').show();

                // Make rental price fields required (at least one)
                addRentalValidation();
            } else if (productType === 'refurbished') {
                console.log('Showing refurbished fields');
                $('.refurbished-section').show();
                $('.refurbished-field').closest('.form-row').show();

                // Add visual indicator for condition field
                highlightConditionField();
            }
        }

        // Add validation message for rental products
        function addRentalValidation() {
            var rentalSection = $('.rental-section');

            // Remove any existing validation messages
            rentalSection.find('.rental-validation-msg').remove();

            // Add validation message
            rentalSection.find('h2').after(
                '<p class="rental-validation-msg" style="color: #d63031; font-weight: 600; margin: 10px 0;">' +
                '⚠️ At least one rental price (daily, weekly, or monthly) is required for rental products.' +
                '</p>'
            );
        }

        // Highlight condition field for refurbished products
        function highlightConditionField() {
            var conditionField = $('.refurbished-field').closest('.form-row');

            // Remove any existing highlights
            conditionField.find('.condition-highlight').remove();

            // Add highlight
            conditionField.find('label').after(
                '<span class="condition-highlight" style="color: #f59e0b; font-weight: 600; margin-left: 10px;">' +
                '(Recommended for refurbished products)' +
                '</span>'
            );
        }

        // Run on page load
        toggleConditionalFields();

        // Run when product type changes
        $('input[name="product_type"]').on('change', function() {
            toggleConditionalFields();
        });

        // Also handle when sections are manually expanded/collapsed
        $('.collapse').on('show.bs.collapse', function() {
            setTimeout(toggleConditionalFields, 100);
        });

        // Add visual indicators to product type radio buttons
        $('input[name="product_type"]').each(function() {
            var value = $(this).val();
            var label = $(this).next('label');

            var icons = {
                'new': '🆕',
                'refurbished': '🔧',
                'rental': '📅'
            };

            var colors = {
                'new': '#10b981',
                'refurbished': '#f59e0b',
                'rental': '#3b82f6'
            };

            if (icons[value]) {
                label.html(
                    '<span style="display: inline-block; padding: 8px 15px; border-radius: 8px; border: 2px solid ' + colors[value] + '; background: ' + ($(this).is(':checked') ? colors[value] : 'white') + '; color: ' + ($(this).is(':checked') ? 'white' : colors[value]) + '; font-weight: 600; cursor: pointer; transition: all 0.3s;">' +
                    icons[value] + ' ' + label.text() +
                    '</span>'
                );
            }
        });

        // Update radio button styling on change
        $('input[name="product_type"]').on('change', function() {
            $('input[name="product_type"]').each(function() {
                var value = $(this).val();
                var label = $(this).next('label');
                var span = label.find('span');

                var colors = {
                    'new': '#10b981',
                    'refurbished': '#f59e0b',
                    'rental': '#3b82f6'
                };

                if ($(this).is(':checked')) {
                    span.css({
                        'background': colors[value],
                        'color': 'white'
                    });
                } else {
                    span.css({
                        'background': 'white',
                        'color': colors[value]
                    });
                }
            });
        });

        console.log('Product conditional fields script initialized');
    });
})(django.jQuery);