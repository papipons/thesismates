function answer(ans){
	startSpinner();
	ajaxPost('answer/', {'answer':ans}, function(content){
		stopSpinner();
    });
}

$(function(){
	$("#answer-form").on('submit', function(e){
		e.preventDefault();
		var ans = $("#answer-form #id_answer").val();
		answer(ans);
	});
})
