$(".edit").on('click', function(e){
	e.preventDefault();

	var secondParent = $(this).parent().parent();
	secondParent.addClass("active");
	$("#account-table tr").not(secondParent).removeClass("active");

	var currentForm = $("#"+this.id+"_form");
	currentForm.show();				

	var passwordFormChildren = $("#password_form").children();

	$(".form-group").not(currentForm).not(passwordFormChildren).hide();

	var currentValue = $("#"+this.id+"_value");
	currentValue.hide();
	$("#account-table span").not(currentValue).show();

});
