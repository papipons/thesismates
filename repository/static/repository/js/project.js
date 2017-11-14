var projectsDataTable = $("#projects-table").DataTable({
	"info" : false,
	"paging" : false,
	"order" : [[1, "asc"]]
});


function addProjectWithMembers(projectTitle,coordinator,users){
	startSpinner();
	console.log(coordinator);

	postData = {
		'title' : projectTitle,
		'coordinator' : coordinator,
		'users' : users
	}

	ajaxPost('add_project/', postData, function(content){
		var targetElement = $("#add-project-form-response");

		if(content.valid == false){
			var failMessage = "Please fill out the forms respectively";
			showFail(failMessage,targetElement);
		} else {
			var successMessage = "Project created successfully!";
			showSuccess(successMessage,targetElement,function(){
				$("#add-project-form #id_title").val('');
				$("#add-project-form #id_user").select2("val", "");
				$("#add-project-form #id_coordinator").select2("val", "");
			});
		}

		stopSpinner();
    });
}

function addEvent(postData){
	postData['course'] = $("#add-event-form #course").val();
	ajaxPost('add_event/', postData, function(content){
		$('#add-event-modal').modal('hide');
    });
}

function assign_advisers(coordinator, faculty){
	var postData = {
		'course' : coordinator,
		'faculty' : faculty
	}

	ajaxPost('assign_advisers/', postData, function(content){
		var targetElement = $("#aaa-form-response");
		if(content.valid == 0){
			var failMessage = content.errors;
			showFail(failMessage,targetElement)
		} else {
			var successMessage = "Assignment added successfully!";
			var output = "";
			output += "<tr>";
			output += "<td>"+content.course+"</td>";
			output += "<td>"+content.coordinator+"</td>";
			output += "<td>None</td>";
			output += "</tr>";

			$("#available-advisers-table tbody").append(output);
		}
    });
}

$(function(){
	$('.django-select2').djangoSelect2();
	$("#filter").djangoSelect2({
		minimumResultsForSearch: Infinity
	});
})

$("#add-project-form").on('submit', function(e){
	e.preventDefault();
	var projectTitle = $("#add-project-form #id_title").val();
	var coordinator = $("#add-project-form #id_coordinator").val();
	var users = $("#add-project-form #id_user").val();
	addProjectWithMembers(projectTitle,coordinator,users);
});

$("#aaa-form").on('submit', function(e){
	e.preventDefault();
	var coordinator = $("#aaa-form #id_coordinator").val();
	var faculty = $("#aaa-form #id_faculty").val();
	assign_advisers(coordinator, faculty)
});

$('#add-project-modal').on('show.bs.modal', function (e) {
	$("#add-project-form #id_title").val('');
	$("#add-project-form #id_coordinator").select2("val", "");
	$("#add-project-form #id_user").select2("val", "");
})

$('#add-event-modal').on('show.bs.modal', function (e) {
	$("#deadline-date-picker").data("DateTimePicker").minDate(moment().add("days", 1));

	$("#add-event-modal input").val('');
	$("#add-event-modal textarea").val('');
})

$("#add-event-form").on('submit', function(e){
	e.preventDefault();

	postData = {}
	active = $("#add-event-modal .tab-content .active").attr('id');

	switch(active){
		case "deadline":
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
	}

	addEvent(postData);
});

$(".datepicker").datetimepicker({
	format: 'MMMM D, YYYY'
});

$(".timepicker").datetimepicker({
	format: 'HH:mm A'
});


