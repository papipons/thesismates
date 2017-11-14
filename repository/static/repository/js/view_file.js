$(function(){
	$("li img").unveil(2000, function() {
	  $(this).load(function() {
	    this.style.opacity = 1;
	  });
	});

});
