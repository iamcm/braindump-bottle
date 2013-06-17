

$(document).ready(function(){
    $('#formRegister').on('submit', function(ev){
        ev.preventDefault();

        var params = $(this).serialize();

        $.post('/register', params, function(json){
            if(json.success==1){
                window.location = '/index.html';
            } else {
                Util.flashMessage('error', json.error);
            }
        })
    })
});