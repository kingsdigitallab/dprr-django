$(document).ready(function() {

	// Expand / Collapse

	$('.panel-head h4').bind("click", function() {
		$(this).parent().next('.panel-body').slideToggle(400).removeClass("hidden");
		$("i", this).toggleClass("fa-caret-down fa-caret-right");
		return false;
	});

});