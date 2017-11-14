function askQuestion(title, description){
	postData = {
		'title' : title,
		'description' : description
	}

	ajaxPost('ask_question/', postData, function(content){

    });
}

$(function(){
	$("#ask-question-form").on('submit', function(e){
		e.preventDefault();
		var title = $("#ask-question-form #id_title").val();
		var description = $("#ask-question-form #id_description").val();
		askQuestion(title, description);
	});

	$("#search-form").on('submit', function(e){
	    e.preventDefault();
	    var data = $("#id_search").val();

	    if(data!=""){
	        postData = {
	            'search' : data
	        };
	        getSearchResults(postData);
	    } else {
	        console.log("nope!");
	    }
	});
})
