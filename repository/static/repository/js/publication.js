function removeFile(url){
    ajaxPost(url, {}, function(content){
        startSpinner();
        $('#file-'+content['fileid']).remove();
        $("#storage-gauge").css('width',content['percentage']+'%');
        $("#storage-gauge-label").html(content['used_storage_size']);
        $("#storage-percentage").html(content['percentage']+'%');

        if(content['used_storage_size'] == 0){
            $("#no-doc").show();
        } else {
            $("#no-doc").hide();
        }

        reached_cap = false
        $("#full-notification").hide();

        if($("#reached-cap-notification:visible")){
            $("#reached-cap-notification").hide();
        }

        if($("#insuff-space-notification:visible")){
            $("#insuff-space-notification").hide();
        }

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

function upload_files(url, formData){
    startSpinner();
    $.ajax({
        type: 'POST',
        url : url,
        processData: false,
        contentType: false,
        enctype: "multipart/form-data",
        data  : formData,
        success: function(data) {
            if(data.valid == true){
                var files = data.files;
                for(x in files){
                    var container = $("#content #files-container");
                    var output = '';
                    output += "<tr id='file-"+files[x].id+"'>";
                    output += "<td>"+files[x].name+"</td>";
                    output += "<td>"+files[x].uploaded_by+"</td>";
                    output += "<td>"
                    output += '<a class="btn btn-info btn-xs" target="_blank" href="view/'+files[x].id+'">Open</a>';
                    output += '<a class="btn btn-warning btn-xs" href="download/'+files[x].id+'">Download</a>';
                    output += '<a class="btn btn-danger btn-xs delete-file" target="_blank" href="'+data.url+'/delete_file/'+files[x].id+'">Delete</a>';
                    output += "</td>"
                    output += "</tr>";

                    $("#no-doc").hide();
                    container.append(output);
                    stopSpinner();
                }
            } else if (data.valid == false){
                var failMessage = "";
                failMessage += "<h6 class='text-danger'>";
                failMessage += '<i class="fa fa-exclamation-circle"></i>';
                failMessage += ' One pdf file only';
                failMessage += "</h6>";
                showFail(failMessage,$("#form-response"));
                stopSpinner();
            }
        }
    })
}

function startConfirmationProcess(){
    startSpinner();
    ajaxPost('start_confirmation/', {}, function(content){
        stopSpinner();
    });
}

function startProcessing(){
    startSpinner();
    ajaxPost('start_processing/', {}, function(content){
        stopSpinner();
    });
}

function rejection(){
    startSpinner();
    ajaxPost('rejection/', {}, function(content){
        stopSpinner();
    });
}

$(function(){
    $('a[title]').tooltip();
})

$("#reject").on('click', function(e){
    $("#reject-notification").show();
})

$("#content").unbind().on('click', '#add-pdf-file', function(e){
    e.preventDefault();
    $("#id_docfile").trigger('click');
});

$('#id_docfile').on('change', function(e){
    $("#add-file-form").submit();
});

$("#add-file-form").on('submit', function(e){
    e.preventDefault();
    var csrf_token = $('input[name="csrfmiddlewaretoken"]').val();
    var url = $(this).attr('action');
    var formData = new FormData($('#add-file-form')[0]);
    formData.append("csrfmiddlewaretoken", csrf_token);
    upload_files(url, formData);
})

$('#files-container').on('click', ".delete-file", function(e){
    e.preventDefault();
    var url = $(this).attr('href');
    removeFile(url);
});

$("#content").on('click', '#send-notification', function(e){
    e.preventDefault();
    swal({
      title: "Send notification to coordinator?",
      text: "If the coordinator confirmed the list of official documents, working files would not be retrievable anymore. Do you want to continue?",
      type: "warning",
      showCancelButton: true,
      confirmButtonClass: 'btn-warning',
      confirmButtonText: 'Confirm'
    }, function(){
        startConfirmationProcess();
    });
});

$("#content").on('click', '#confirm', function(e){
    e.preventDefault();
    swal({
      title: "Confirm official document list?",
      text: "After confirmation, working files will be deleted and official documents will be processed. It is irreversable",
      type: "warning",
      showCancelButton: true,
      confirmButtonClass: 'btn-warning',
      confirmButtonText: 'Confirm'
    }, function(){
        startProcessing();
    });
});

$("#content").on('click', '#reject', function(e){
    e.preventDefault();
    swal({
      title: "Reject official document list?",
      text: "After rejection, students should upload the required files.",
      type: "warning",
      showCancelButton: true,
      confirmButtonClass: 'btn-warning',
      confirmButtonText: 'Reject'
    }, function(){
        rejection();
    });
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

