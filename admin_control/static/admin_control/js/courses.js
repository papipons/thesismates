var coursesDataTable = $("#courses-table").DataTable({
	"lengthMenu": [[10, 20, 30, 40, 50, -1], [10, 20, 30, 40, 50, "All"]]
});

$("#courses-table_length select").djangoSelect2({
	minimumResultsForSearch: Infinity
});

$('.django-select2').djangoSelect2();

function getDateToString(){
	var dateString = '';
	var d = new Date();
	var months = [
		'January','February','March','April','May','June',
		'July','August','September','October','November','December'
	];
	var month = months[d.getMonth()];
	var date = d.getDate();
	var year = d.getFullYear().toString();

	dateString = month +" "+ date + ", " + year;

	return dateString;
}

function reloadContent(){
	ajaxPost('courses/', {}, function(content){
        $("#manage-content").html(content);
    });
}

function addCourse(postData){
	ajaxPost('add_course/', postData, function(content){
		var targetElement = $("#add-course-form-response")
		if(content.valid == false){
			console.log(content.error)
			var failMessage = content.errors.name;
			showFail(failMessage,targetElement);
		} else {
			var successMessage = "Course added successfully!";
			showSuccess(successMessage,targetElement,function(){
				coursesDataTable.row.add([
					postData['name'],
					content.code,
					getDateToString()
				]).draw();

				$("#add-course-form #id_name").val('');
			});
		}
    });
}

function editCourse(newName){
	var originalName = coursesDataTable.row('tr.active').data();
	originalName = originalName[0];
	var postData = {
		'originalName': originalName,
		'newName': newName
	};
	
	ajaxPost('edit_course/', postData, function(content){
		var targetElement = $("#edit-course-form-response")
		targetElement.html("Successfully updated " + originalName + " to " + newName);
		setTimeout(function(){
			reloadContent();
		},1000);
    });
}

$("#add-course-form").on('submit', function(e){
	e.preventDefault();
	var postData = {
		'name' : $("#add-course-form #id_name").val(),
		'program' : $("#add-course-form #id_program").val(),
		'text' : $("#add-course-form #id_program option:selected").text()
	};
	addCourse(postData);
});

$('#edit-course-form').on('submit', function(e){
	e.preventDefault();
	var newName = $("#edit-course-form #id_name").val();
	editCourse(newName);
});

$('#courses-table tbody tr').on( 'click', function () {
	var selectedData = coursesDataTable.row(this).data();
	selectedDataName = selectedData[0];

	$("#edit-course-form #id_name").val(selectedDataName);

    if ( $(this).hasClass('active') ) {
        $(this).removeClass('active');
        $("#edit-course-form #id_name").val("");
    }
    else {
        coursesDataTable.$('tr.active').removeClass('active');
        $(this).addClass('active');
    }
});
