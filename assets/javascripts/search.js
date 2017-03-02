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
          return value +
            ' <span class="label radius">' +
            item.count +
            "</span>";
        }
      },
      //placeholder: $input.attr('title')
      list: {
        match: {
          enabled: true,
          method: function(element, phrase) {
            if (element.indexOf(phrase) === 0) {
              return true;
            } else {
              return false;
            }
          }
        },
        maxNumberOfElements: 100,
        sort: { enabled: true },
        onChooseEvent: function() {
          $input.closest("form").submit();
        }
      }
    };

    $input.easyAutocomplete(options);
  },
  init: function() {
    self = this;
    $("input.autocomplete").each(function() {
      self.setUp(this);
    });
  }
};

$(document).ready(function() {
  autocomplete.init();
});

