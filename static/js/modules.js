$(document).ready(function() {
    var icon = $('.play-button');
    icon.click(function() {
        console.log("I m clicked !", $(this));
        $(this).parent(".play_thumb").hide();
        iframe = $(this).parent(".play_thumb").siblings('iframe');
        iframe.show()
        if (iframe.data('src')){ // only do it once per iframe
            iframe.prop('src', iframe.data('src')+'?autoplay=1').data('src', false);
            console.log("iframe src = ", iframe.attr('src'))
            }
        
        return true;
    });
});