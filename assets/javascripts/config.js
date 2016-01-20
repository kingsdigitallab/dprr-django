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

	// Off-canvas open by default
	// $('.off-canvas-wrap').foundation('offcanvas', 'show', 'move-right');
	$('.off-canvas-wrap').foundation('offcanvas', 'hide', 'move-right');
	$('.off-canvas-wrap').foundation('offcanvas', 'toggle', 'move-right');

});