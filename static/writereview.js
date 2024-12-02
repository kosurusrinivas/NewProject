$(document).ready(function() {
	$('.selector > .selection').click(function(e) {
		$(this).siblings().removeClass('selected');
		$(this).addClass('selected'); 
	});
});