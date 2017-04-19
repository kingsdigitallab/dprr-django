$(document).ready(function () {

    // Expand / Collapse

    $('.panel-head h4').bind("click", function () {
        $(this).parent().next('.panel-body').slideToggle(400).removeClass("hide");
        $("i", this).toggleClass("fa-caret-down fa-caret-right");
        return false;
    });

    $('.expander').bind("click", function () {
        $(this).next('.collapsible').slideToggle(400).removeClass("hide");
        $("i", this).toggleClass("fa-caret-down fa-caret-right");
        $(".expander ~ span.info").toggleClass("hide show");
        return false;
    });

    $('button.options').bind("click", function () {
        var txt = $(".search-box").is(':visible') ? 'Show' : 'Hide';
        $('.search-box').slideToggle(400);
        $('#showhide').text(txt);
        // toggle extra-margin class to remove blank space when collapsing
        // the search box
        // $('#search-results-box').toggleClass("extra-margin");
        return false;
    });

    // Printing search results
    $('#printme').bind("click", function () {
        // Trigger reload with minimal pagination for printing
        var separator = '?';
        if (document.URL.includes("?")) {
            separator = '&';
        }
        if (document.URL.includes("#")) {
            new_url = document.URL.split("#");
            document.location.href = new_url[0] + separator + 'printme=1#' + new_url[1]; // Safe as if URL includes split, we have at least 2 elements.
        } else {
            document.location.href = document.URL + separator + 'printme=1'
        }


    });
    if (document.URL.includes("printme")) {
        //Print the reloaded page
        window.print();

        var new_url = document.URL;
        if (new_url.includes("&printme=1"))
        {
            new_url = new_url.replace('&printme=1', '');
        } else if (new_url.includes("?printme=1&"))
        {
            new_url = new_url.replace('?printme=1&', '?');
        } else if (new_url.includes("?printme=1"))
        {
            new_url = new_url.replace('?printme=1', '');
        }

        window.location.href=new_url;


    }

});
