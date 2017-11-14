var reached_cap = false;

$(function(){

    if($("#full-notification").hasClass('reached')){
        reached_cap = true
        $("#full-notification").show();
    }

    function removeFile(url){
        startSpinner();
        ajaxPost(url, {}, function(content){
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
                if(data.valid == false) {
                    $("#insuff-space-notification").show();
                    stopSpinner();
                }
                
                if(data.valid == true){
                    ajaxPost("files", {}, function(content){
                        $("#profile-content").html(content);
                        stopSpinner();
                    });
                }
            }
        })
    }

    $("#profile-content").unbind().on('click', '#add-file', function(e){
        e.preventDefault();
        if(reached_cap == false){
            $("#id_docfile").trigger('click');
        } else {
            $("#reached-cap-notification").show();
        }
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

})
