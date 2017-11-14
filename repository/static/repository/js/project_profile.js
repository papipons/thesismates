$(function(){
    $('.django-select2').djangoSelect2();
    $('a[title]').tooltip();

})



function getPartial(partialName){
    startSpinner();
    ajaxPost(partialName, {}, function(content){
        $("#profile-content").html(content);
        stopSpinner();
    });
}

function sendRequest(){
    startSpinner();
    ajaxPost('doc_req/', {}, function(content){
        getPartial('documentation');
    });
}

function addMembers(user){
	postData = {
		'user' : user
	}

    startSpinner();
    ajaxPost('add_member/', postData, function(content){
        var targetElement = $("#add-member-form-response");

        if(content.valid == false){
            var failMessage = "Please fill out the forms respectively";
            showFail(failMessage,targetElement);
        } else {
            $("#add-member-modal").modal('toggle');
            setTimeout(function(){
               ajaxPost('profile', {}, function(content){
                   $("#profile-content").html(content);
                   stopSpinner();
               });
            }, 1000)
		}
    });
}

function requestAdviser(postData){
    startSpinner();
    ajaxPost('request_adviser/', postData, function(content){

        stopSpinner();
    });
}

function startPublicationProcess(){
    startSpinner();
    ajaxPost('start_publication', {}, function(content){
        stopSpinner();
    });
}

function editTitle(postData){
    startSpinner();
    ajaxPost('edit_title/', postData, function(content){
        var failMessage = content.error;
        showFail(failMessage,$("#title-error"));
        stopSpinner();
    });

}

function editAbstract(postData){
    startSpinner();
    ajaxPost('edit_abstract/', postData, function(content){

        if(content.valid == true){
            $("#abstract").html(content.new_abstract);
            $("#id_abstract").html(content.new_abstract);

            $("#edit-abstract-form").hide();
            $("#notifier").hide();
            $("#edit-abstract").show();
            $("#abstract").show();
        }  else {
            showFail(content.error,$("#abstract-error"));
        }
        
        stopSpinner();
    });
}

function leaveGroup(id){
    ajaxPost('leave_group', {'id':id}, function(content){
        ajaxPost('profile', {}, function(content){
            $("#profile-content").html(content);
            stopSpinner();
        });
    });
}

function getToDeleteMessage(id){
    startSpinner();
    var message = "";
    ajaxPost('get_user_for_delete', {'id':id}, function(content){
        stopSpinner();
        var message = content['message'];
        swal({
          title: message,
          text: "",
          type: "warning",
          showCancelButton: true,
          confirmButtonClass: 'btn-warning',
          confirmButtonText: 'Confirm'
        }, function(){
            startSpinner();
            leaveGroup(id);
        });
    });
}

getPartial('profile');

$(".profile-link").on('click', function(e){
	e.preventDefault();
	$(this).blur();
	$(this).addClass('active');
	$(this).siblings().removeClass('active');
	
	var partialName = $(this).attr('id');
	getPartial(partialName);

});

$('#edit-title-form').on('submit', function(e){
    e.preventDefault();
    var title = $("#id_title").val();
    if(title != ""){
        postData = {
            'title' : title
        };

        editTitle(postData);
    } else {
        $("#title-holder").show();
        $("#edit-title-form").hide();
    }
});

$("#edit-project-title").on('click', function(e){
    e.preventDefault();
    $("#title-holder").hide();
    $("#edit-title-form").show();
});

$("#profile-content").on('click', '#edit-abstract', function(e){
    e.preventDefault();
    $("#abstract").hide();
    $("#edit-abstract").hide();
    $("#edit-abstract-form").show();
    $("#notifier").show();
});

$("#profile-content").on('submit', '#edit-abstract-form', function(e){
    e.preventDefault();
    var abstract = $("#id_abstract").val();
    postData = {
        'abstract' : abstract
    };
    editAbstract(postData);
});

$('#add-member-modal').on('show.bs.modal', function (e) {
	$("#add-member-form #id_user").select2("val", "");
})


$("#request-adviser-form").on('submit', function(e){
    e.preventDefault();
    var faculty = $("#faculty").val();
    postData = {
        'faculty' : faculty
    };
    requestAdviser(postData);
});

$("#profile-content").on('click', ".leave-group", function(e){
    var to_remove = $(this).attr('id');
    getToDeleteMessage(to_remove);
});

$("#content").on('click', '#doc_req', function(e){
    e.preventDefault();
    sendRequest();
});

    
$("#content").on('click', '#start-publication-process', function(e){
    e.preventDefault();
    swal({
      title: "Start publication process?",
      text: "Starting the publication process is irreversable",
      type: "warning",
      showCancelButton: true,
      confirmButtonClass: 'btn-warning',
      confirmButtonText: 'Confirm'
    }, function(){
        startPublicationProcess();
    });
});



