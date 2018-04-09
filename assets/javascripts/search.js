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
        maxNumberOfElements: 500,
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

var getUrlParameter = function getUrlParameter(sParam) {
    var sPageURL = decodeURIComponent(window.location.search.substring(1)),
        sURLVariables = sPageURL.split('&'),
        sParameterName,
        i;

    for (i = 0; i < sURLVariables.length; i++) {
        sParameterName = sURLVariables[i].split('=');

        if (sParameterName[0] === sParam) {
            return sParameterName[1] === undefined ? true : sParameterName[1];
        }
    }
};

$(document).ready(function() {
  if(autocomplete !== undefined)
  {
    autocomplete.init();
  }

  $('body').on('change', '.switch', function()
  {
    // 150ms delay - this should match foundation's transition speed
    var timer = window.setTimeout(function() { $('form').submit(); }, 150);
  });

   var href = window.location.href;
    if (href.indexOf('page=') > 0) {
        var top = $('#search-results-box').offset().top;
        $('html, body').scrollTop(top);
    }


});

