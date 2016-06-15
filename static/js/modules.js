$(document).ready(function() {
    // play button 
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
    
    // Watch scrollspy events and change breadcrumb
    $('#accordion ul.list-group > li').on("activate.bs.scrollspy", function(){
        console.log("Link activated by spy", $(this));
        section_title = $(this).parent().parent().children('h4').children('a').text();
        //subsec_title = $(this).children('a').text()
        $('ol.breadcrumb').children('.active').text(section_title);        
    });
    
});