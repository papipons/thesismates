function highlight_keywords(keywords){
    array = keywords.split(" ");
    array.forEach(function(each){
        $(".project-titles").highlight(each);
    });
}

function getSearchResults(postData, keywords){
    startSpinner();
    ajaxPost("search/", postData, function(content){
        $("#projects").html(content);
        highlight_keywords(keywords);    
        $(".per-title").clamp();
        $(".per-desc").clamp();
        stopSpinner();    
    });
}

$(function(){
    $("#search-form").on('submit', function(e){
        e.preventDefault();
        var data = $("#id_search").val();

        if(data!=""){
            var postData = {
                'search' : data
            };
            getSearchResults(postData, data);
        } else {
            console.log("nope!");
        }
    });
})
