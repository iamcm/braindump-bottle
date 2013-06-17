// Convert divs to queue widgets when the DOM is ready
$(function() {
    $("#uploader").pluploadQueue({
        // General settings
        runtimes : 'html5,flash',
        url : '/upload',
        max_file_size : '10mb',
        chunk_size : '1mb',
        unique_names : true,

        // Resize images on clientside if we can
        resize : {width : 320, height : 240, quality : 90},

        // Flash settings
        flash_swf_url : 'static/plupload/js/plupload.flash.swf'
    });

    // Client side form validation
    /*$('form').submit(function(e) {
        var uploader = $('#uploader').pluploadQueue();

        // Files in queue upload them first
        if (uploader.files.length > 0) {
            // When all files are uploaded submit form
            uploader.bind('StateChanged', function() {
                if (uploader.files.length === (uploader.total.uploaded + uploader.total.failed)) {
                    $('form')[0].submit();
                }
            });
                
            uploader.start();
        } else {
            alert('You must queue at least one file.');
        }

        return false;
    });*/
});