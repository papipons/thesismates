$(function(){
	function addEvent(postData){
		startSpinner();
		ajaxPost('add_event/', postData, function(content){
			getPartial('calendar');
			$('#add-event-modal').modal('hide');
			stopSpinner();
	    });
	}

	function getEventInstance(id){
		startSpinner();
		ajaxPost('get_event_instance/', {'id':id}, function(content){
			$("#edit-form-container").html(content);

			$(".datepicker").datetimepicker({
				format: 'MMMM D, YYYY'
			});

			$(".timepicker").datetimepicker({
				format: 'HH:mm A'
			});
			$("#edit-event-modal").modal();
			stopSpinner();
	    });
	}

	function saveManual(postData){
		startSpinner();
		ajaxPost('save_manual/', postData, function(content){
			getPartial('calendar');
			$('#edit-event-modal').modal('hide');
			stopSpinner();
	    });
	}

	function saveEventChanges(event){
		startSpinner();
		var start = event.start.format('YYYY-MM-DD');
		var end = event.end.format('YYYY-MM-DD');

		var postData = {
			'id' : event.id,
			'start' : start,
			'end' : end
		};

		ajaxPost('save_event_changes/', postData, function(content){
			getPartial('calendar');
			stopSpinner();
		});
	}

	function removeEvent(event){
		startSpinner();
		ajaxPost('remove_event/', {'id':event.id}, function(content){
			getPartial('calendar');
			stopSpinner();
	    });
	}

	function viewEventDetails(event){
		$("#modalTitle").html(event.title);
		$("#eventNotes").html(event.notes);
		$("#postedBy").html(event.posted_by);

		if(event.members){
			$("#includedMembers").html('');
			event.members.forEach(function(each){
			    $("#includedMembers").append(each+"<br>");
			});

			$("#includedMembers").prepend("<br><span><strong>Included Members:</strong></span><br>");
		} else {
			$("#includedMembers").html('');
		}

		$("#type").html(event.type);

		$("#event-details-modal").modal();
	}

	var projectUID = $("#project-uid").text();
	var calendar = $('#calendar-holder').fullCalendar({
		events: 'get_events?projectUID='+projectUID,
		defaultView: 'month',
		eventLimit: true,
		header: {
			left: 'prev,next today',
			center: 'title',
			right: 'month,basicWeek,basicDay'
		},
		views: {
			month: {
				timeFormat: ' ',
			},
		},
		eventClick:  function(event) {
			viewEventDetails(event)
	    },
	    eventDrop: function(event){
	    	saveEventChanges(event);
	    },
	    eventDragStop: function(event, jsEvent){
	    	var trash = $('body #trash');
	    	
		    var ofs = trash.offset();

		    var x1 = ofs.left;
		    var x2 = ofs.left + trash.outerWidth(true);
		    var y1 = ofs.top;
		    var y2 = ofs.top + trash.outerHeight(true);

		    if (jsEvent.pageX >= x1 && jsEvent.pageX<= x2 && jsEvent.pageY>= y1 && jsEvent.pageY <= y2) {
		        removeEvent(event);
		    }
	    }
	});

	$(".datepicker").datetimepicker({
		format: 'MMMM D, YYYY'
	});

	$(".timepicker").datetimepicker({
		format: 'HH:mm A'
	});

	$("body").unbind().on('submit', '#add-event-form', function(e){
		e.preventDefault();

		postData = {}
		active = $("#add-event-modal .tab-content .active").attr('id');

		switch(active){
			case "deadline":
				console.log('test');
				postData['event_type'] = "deadline"
				postData['title'] = $("#add-event-form #id_add-deadline-event-form-title").val();

				var deadlineDate = $("#add-event-form #id_add-deadline-event-form-start_date").val();
				postData['start_date'] = moment(deadlineDate, 'MMMM D, YYYY').format('YYYY-MM-DD');

				var deadlineTime = $("#add-event-form #id_add-deadline-event-form-start_time").val();
				postData['start_time'] = moment(deadlineTime, 'HH:mm A').format('HH:mm:ss');

				var notes = $("#add-event-form #id_add-deadline-event-form-notes").val();
				
				if(notes==""){
					postData['notes'] = "No notes";
				} else {
					postData['notes'] = notes
				}

				break;

			case "journal":
				var includedMembers = $('#add-event-form .included-members:checked').map(function() {
					return this.value;
				}).get();

				postData['included_members'] = includedMembers;

				postData['event_type'] = "journal"
				postData['title'] = $("#add-event-form #id_add-journal-event-form-title").val();

				var startDate = $("#add-event-form #id_add-journal-event-form-start_date").val();
				postData['start_date'] = moment(startDate, 'MMMM D, YYYY').format('YYYY-MM-DD');
				postData['end_date'] = moment(startDate, 'MMMM D, YYYY').format('YYYY-MM-DD');

				notes = $("#add-event-form #id_add-journal-event-form-notes").val();

				if(notes==""){
					postData['notes'] = "No notes";
				} else {
					postData['notes'] = notes
				}

				break;
		}

		addEvent(postData);

	});;
	$("#master-content").unbind().on('submit', '#edit-event-form', function(e){
		e.preventDefault();
		var type = $("#event-type").html();

		postData = {}

		var id = $("#edit-event-form #event-id").html();
		postData['id'] = id

		switch(type){
			case "deadline":
				postData['title'] = $("#edit-event-form #id_edit-deadline-event-form-title").val();

				var deadlineDate = $("#edit-event-form #id_edit-deadline-event-form-start_date").val();
				postData['start_date'] = moment(deadlineDate, 'MMMM D, YYYY').format('YYYY-MM-DD');

				var deadlineTime = $("#edit-event-form #id_edit-deadline-event-form-start_time").val();
				postData['start_time'] = moment(deadlineTime, 'HH:mm A').format('HH:mm:ss');

				var notes = $("#edit-event-form #id_edit-deadline-event-form-notes").val();
				
				if(notes==""){
					postData['notes'] = "No notes";
				} else {
					postData['notes'] = notes
				}

				break;

			case "journal":
				var includedMembers = $('#edit-event-form .included-members:checked').map(function() {
					return this.value;
				}).get();

				postData['included_members'] = includedMembers;

				postData['event_type'] = "journal"
				postData['title'] = $("#edit-event-form #id_edit-journal-event-form-title").val();

				var startDate = $("#edit-event-form #id_edit-journal-event-form-start_date").val();
				postData['start_date'] = moment(startDate, 'MMMM D, YYYY').format('YYYY-MM-DD');
				postData['end_date'] = moment(startDate, 'MMMM D, YYYY').format('YYYY-MM-DD');

				notes = $("#edit-event-form #id_edit-journal-event-form-notes").val();

				if(notes==""){
					postData['notes'] = "No notes";
				} else {
					postData['notes'] = notes
				}
				break;
		}
		saveManual(postData);
	});

	$('#add-event-modal').on('show.bs.modal', function (e) {

		$("#deadline-date-picker").data("DateTimePicker").minDate(moment().add("days", 1));
		
		$("#journal-start-date-picker").data("DateTimePicker").maxDate(moment());

		$("#add-event-modal input:text").val('');
		$("#add-event-modal textarea").val('');
	})

	$(".edit-event").on('click', function(e){
		e.preventDefault();
		getEventInstance($(this).attr('id'));
	})
})
