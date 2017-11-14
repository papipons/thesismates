var programsDataTable = $("#program-table").DataTable({
	"lengthMenu": [[10, 20, 30, 40, 50, -1], [10, 20, 30, 40, 50, "All"]]
});

$("#program-table_length select").djangoSelect2({
	minimumResultsForSearch: Infinity
});

function reloadContent(){
	ajaxPost('programs/', {}, function(content){
        $("#manage-content").html(content);
    });
}


function editProgram(postData){
	ajaxPost('edit_program/', postData, function(content){
		var targetElement = $("#edit-program-form-response")
		targetElement.html("Successfully updated " + postData[0] + " to " + postData[1]);
		setTimeout(function(){
			reloadContent();
		},1000);
    });
}

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

function addProgram(postData){
	ajaxPost('add_program/', postData, function(content){
		var targetElement = $("#add-program-form-response")
		if(content.valid == false){
			var failMessage = content.errors.name;
			showFail(failMessage,targetElement);
		} else {
			var successMessage = "Program added successfully!";
			showSuccess(successMessage,targetElement,function(){
				programsDataTable.row.add([
					postData['code'],
					postData['name'],
					postData['description'],
					getDateToString()
				]).draw();

				$("#add-program-form #id_name").val('');
				$("#add-program-form #id_code").val('');
				$("#add-program-form #id_description").val('');
			});
		}
    });
}

$("#add-program-form").on('submit', function(e){
	e.preventDefault();
	var postData = {
		'name' : $("#add-program-form #id_name").val(),
		'code' : $("#add-program-form #id_code").val(),
		'description' : $("#add-program-form #id_description").val(),
 	}
	addProgram(postData);
});

$('#edit-program-form').on('submit', function(e){
	e.preventDefault();
	var originalName = programsDataTable.row('tr.active').data();
	originalName = originalName[1];
	var code = $("#edit-program-form #id_code").val();
	var name = $("#edit-program-form #id_name").val();
	var desc = $("#edit-program-form #id_description").val();

	postData = {
		'originalName' : originalName,
		'name' : name,
		'code' : code,
		'desc' : desc
	}

	editProgram(postData);
});

$('#program-table tbody tr').on( 'click', function () {
	var selectedData = programsDataTable.row(this).data();
	selectedDataCode = selectedData[0];
	selectedDataName = selectedData[1];
	selectedDataDesc = selectedData[2];

	$("#edit-program-form #id_code").val(selectedDataCode);
	$("#edit-program-form #id_name").val(selectedDataName);
	$("#edit-program-form #id_description").val(selectedDataDesc);

    if ( $(this).hasClass('active') ) {
        $(this).removeClass('active');
        $("#edit-program-form #id_code").val("");
        $("#edit-program-form #id_name").val("");
        $("#edit-program-form #id_description").val("");
    }
    else {
        programsDataTable.$('tr.active').removeClass('active');
        $(this).addClass('active');
    }
});