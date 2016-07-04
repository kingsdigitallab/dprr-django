var autocomplete = {
    // options for the EasyAutocomplete API
    setUp: function(input) {
        $input = $(input);

        options = {
            adjustWidth: false,
            data: autocompleteDict[$input.attr("name")],
            getValue: "name",
            template: {
                type: "custom",
                method: function(value, item) {
                    return value + ' <span class="label radius">' + item.count + '</span>';
                }
            },
            list: {
                match: {
                    enabled: true
                },
                sort: {
                    enabled: true
                },
                onSelectItemEvent: function() {
                    $input.closest('form').submit();
                }
            },
            placeholder: $input.attr("name")
        };

        $input.easyAutocomplete(options);
    },

    init: function() {
        self = this;
        $('input.autocomplete').each(function() {
            self.setUp(this);
        })
    }
}

$(document).ready(function() {
    autocomplete.init();
});
