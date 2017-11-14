var usersDataTable = $("#users-table").DataTable({
	"lengthMenu": [[10, 20, 30, 40, 50, -1], [10, 20, 30, 40, 50, "All"]]
});

$("#users-table_length select").djangoSelect2({
	minimumResultsForSearch: Infinity
});

function addUser(email){
	ajaxPost('add_user/', {'email': email}, function(content){
		console.log(content.response);
		var targetElement = $("#add-user-form-response")
		if(content.valid == false){
			var failMessage = content.errors;
			showFail(failMessage,targetElement);
		} else {
			var successMessage = "Invitation sent!";
			showSuccess(successMessage,targetElement,function(){
				$("#add-user-form #id_email").val('');
			});
		}
    });
}

$("#add-user-form").on('submit', function(e){
	e.preventDefault();
	var email = $("#add-user-form #id_email").val();
	addUser(email);
});
