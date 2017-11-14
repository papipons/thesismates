function saveSettings(){
	var newSem = $("#id_sem-form-value option:selected").val();
	var sy = $("#id_sy-form-value option:selected").val();
	var capacity = $("#id_capacity-form-value").val();

	var postData = {
		'sem' : newSem,
		'sy' : sy,
		'capacity' : capacity
	};

	console.log(postData);

	ajaxPost('save_settings/', postData, function(content){
		var targetElement = $("#settings-form-response");
		var successMessage = "Settings Saved!";
		showSuccess(successMessage,targetElement,function(){

		});
    });
}

$('.django-select2').djangoSelect2({
	minimumResultsForSearch: Infinity
});

$('#settings-form').on('submit', function(e){
	e.preventDefault();
	saveSettings();
});
