var projectsDataTable = $("#projects-table").DataTable({
	"lengthMenu": [[10, 20, 30, 40, 50, -1], [10, 20, 30, 40, 50, "All"]],
});

$(function(){
	$('.django-select2').djangoSelect2();
	$("#filter").djangoSelect2({
		minimumResultsForSearch: Infinity
	});
	$("#projects-table_length select").djangoSelect2({
		minimumResultsForSearch: Infinity
	});
})
