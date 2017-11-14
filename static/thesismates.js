$(function(){
	$(".per-title").clamp();
	$(".per-desc").clamp();
	
	$(window).on('resize', function(){
		$(".per-title").clamp();
		$(".per-desc").clamp();
	});
})

$("input").alphanum({
	allow: "@'.-_:?"
});

$.fn.modal.Constructor.prototype.enforceFocus = function() {};

var negative = "color:red;";
var positive = "color:green;";
	
$('[data-toggle="tooltip"]').tooltip();

var opts = {
  lines: 13 // The number of lines to draw
, length: 28 // The length of each line
, width: 14 // The line thickness
, radius: 42 // The radius of the inner circle
, scale: 1 // Scales overall size of the spinner
, corners: 1 // Corner roundness (0..1)
, color: '#006CB7' // #rgb or #rrggbb or array of colors
, opacity: 0.25 // Opacity of the lines
, rotate: 0 // The rotation offset
, direction: 1 // 1: clockwise, -1: counterclockwise
, speed: 1 // Rounds per second
, trail: 60 // Afterglow percentage
, fps: 20 // Frames per second when using setTimeout() as a fallback for CSS
, zIndex: 2e9 // The z-index (defaults to 2000000000)
, className: 'spinner' // The CSS class to assign to the spinner
, top: '50%' // Top position relative to parent
, left: '50%' // Left position relative to parent
, shadow: false // Whether to render a shadow
, hwaccel: false // Whether to use hardware acceleration
, position: 'absolute' // Element positioning
};

var target = document.getElementById('loader');
var spinner = new Spinner(opts);

function startSpinner(){
	spinner.spin(target);
	$(target).show();
}

function stopSpinner(){
	spinner.stop();
	$(target).hide();
}

function showFail(failMessage,targetElement){
    targetElement.html(failMessage);
    targetElement.removeClass('text-success');
    targetElement.addClass('text-danger');

    setTimeout(function(){
     targetElement.html('');
    },2000);
}

function showSuccess(successMessage,targetElement,callback){
	targetElement.html(successMessage);
	targetElement.removeClass('text-danger');
	targetElement.addClass('text-success');
	
	 callback();

	setTimeout(function(){
	 targetElement.html('');
	},2000);
}

$('.alert .close-notif').on('click', function(e) {
    $(this).parent().hide();
});
