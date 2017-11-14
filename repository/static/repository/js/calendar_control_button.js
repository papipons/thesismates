	$('.fc-toolbar .fc-left').prepend(
		$('<button type="button" class="fc-button fc-state-default fc-corner-left fc-corner-right"><i class="fa fa-plus"></i></button>')
		.on('click', function(){
			$('#add-event-modal').modal();
		})
	);

	$('.fc-toolbar .fc-left').append(
		$('<button id="trash" type="button" class="fc-button fc-state-default fc-corner-left fc-corner-right"><i class="fa fa-trash"></i></button>')
	);
