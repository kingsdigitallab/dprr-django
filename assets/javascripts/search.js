$( document ).ready(function() {

    var options = {
        data: nomen_list,
        // placeholder: "Nomen",
        getValue: "name",
        template: {
            type: "custom",
            method: function(value, item) {
                return item.name + "(" + item.count + ")";
            }
        },
        list: {
            match: {
                enabled: true
            }
        },
        sort: {
            enabled: true
        }
    };

    $("#id_nomen").easyAutocomplete(options);
});