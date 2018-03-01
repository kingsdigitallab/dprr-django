$(document).ready(function () {

    /*---------------------------------------------------- */
    /* Cookies disclaimer
    /* https://github.com/js-cookie/js-cookie
    ------------------------------------------------------ */

    $(document).ready(function() {
      if (!Cookies.get('dprr-cookie')) {
          $("#cookie-disclaimer").removeClass('hide');
      }
      // Set cookie
      $('#cookie-disclaimer .closeme').on("click", function() {
          Cookies.set('dprr-cookie', 'dprr-cookie-set', {
              expires: 30
          });
      });

      $('.closeme').bind("click", function () {
        $('#cookie-disclaimer').addClass("hide");
        return false;
      });
    });

    // Expand / Collapse

    $('.panel-head h4').bind("click", function () {
        $(this).parent().next('.panel-body').slideToggle(400).toggleClass("hide show");
        $("i", this).toggleClass("fa-caret-down fa-caret-right");
        return false;
    });

    $('.expander').bind("click", function () {
        $(this).next('.collapsible').slideToggle(400).toggleClass("hide show");
        $("i", this).toggleClass("fa-caret-down fa-caret-right");
        $(".expander ~ span.info").toggleClass("hide show");
        return false;
    });

    $('button.options').bind("click", function () {
        var txt = $(".search-box").is(':visible') ? 'Show' : 'Hide';
        $('.search-box').slideToggle(400);
        $('#showhide').text(txt);
        return false;
    });

    // Printing search results
    $('#printme').bind("click", function (event) {
        // Trigger reload with minimal pagination for printing
        event.preventDefault();
        window.print();
    });
});
