function getPartial(partialName){
	// var partial = $("#" + partialName + "_container");
	// partial.removeClass('hide');
	// partial.siblings().addClass('hide');
	startSpinner();
	ajaxPost(partialName+'/', {}, function(content){
        $("#manage-content").html(content);
        stopSpinner();
    });
}

getPartial('programs');

$(".manage-link").on('click', function(e){
	e.preventDefault();
	$(this).addClass('active');
	$(this).siblings().removeClass('active');
	var partialName = $(this).attr('id');

	getPartial(partialName);
});
