

$(document).ready(function(){
    $('#formLogin').on('submit', function(ev){
        ev.preventDefault();

        var params = $(this).serialize();

        $.post('/api/login', params, function(json){
            if(json.success==1){
                window.location = '/index.html';
            } else {
                Util.flashMessage('error', json.error);
            }
        })
    })
});