$(document).ready(function($) {
    $('.people').click(function(event){   

        event.preventDefault();
        $('#vizbox').fadeIn();
        $('html,body').delay(500).animate({scrollTop:$(this.hash).offset().top}, 500);
    });
});
