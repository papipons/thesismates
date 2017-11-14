$('.django-select2').djangoSelect2();


var assignmentsDataTable = $("#assignments-table").DataTable({
	"lengthMenu": [[10, 20, 30, 40, 50, -1], [10, 20, 30, 40, 50, "All"]]
});

$("#assignments-table_length select").djangoSelect2({
	minimumResultsForSearch: Infinity
});

function addAssignment(course,coordinator){
	var postData = {
		'course' : course,
		'faculty' : coordinator,
	};

	ajaxPost('add_assignment/', postData, function(content){
		var targetElement = $("#add-assignment-form-response");
		if(content.valid == 0){
			var failMessage = content.errors;
			showFail(failMessage,targetElement)
		} else {
			var successMessage = "Assignment added successfully!";
			showSuccess(successMessage,targetElement,function(){
				assignmentsDataTable.row.add([
					content.course,
					content.coordinator,
					content.assignment,
					content.semester,
					content.start_school_year + " - " + content.end_school_year
				]).draw();
			});
		}
    });
}

$('#add-assignment-form').on('submit', function(e){
	e.preventDefault();
	var course = $("#add-assignment-form #id_course").val()
	var coordinator = $("#add-assignment-form #id_faculty").val()
	addAssignment(course,coordinator)
});
