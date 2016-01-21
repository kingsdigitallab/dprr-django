$(document).ready(function() {

	// Expand / Collapse

	$('.panel-head h4').bind("click", function() {
		$(this).parent().next('.panel-body').slideToggle(400).removeClass("hide");
		$("i", this).toggleClass("fa-caret-down fa-caret-right");
		return false;
	});

	$('.expander').bind("click", function() {
		$(this).next('.collapsible').slideToggle(400).removeClass("hide");
		$("i", this).toggleClass("fa-caret-down fa-caret-right");
		return false;
	});

	$('button.options').bind("click", function() {
		var txt = $(".search-box").is(':visible') ? 'Show' : 'Hide';
		$('.search-box').slideToggle(400);
		$('#showhide').text(txt);
		return false;
	});

});