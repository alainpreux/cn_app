// compute window height 
function windowSize() {
    var windowHeight = $(window).height() - $('#menutop').height();
    $('.section').css({
        minHeight: windowHeight
    })
}
// reset dynamically window's size
$(window).resize(function() {
    windowSize()
});

$(document).ready(function() {
    // set min height
    windowSize();
    // mini page menu
    $('#header a').click(function() {
        $('.nav li').removeClass('active');
        $(this).parent('li').addClass('active');
        var pageId = $(this).attr('href');
        $('html, body').animate({
            scrollTop: $(pageId).offset().top - $('#menutop').height()
        }, 500);
        return false
    })
    // "voir plus" collapse-like buttons
    $('body').on('show.bs.collapse', function () {
        $('.in').collapse('hide');
    });
    // ?
    // var scrollPos = $('.content #page2').offset().top();
    // $('#page2').html(scrollPos);

})
// $(window).scroll(function() {
//     var scrollCount = $(window).scrollTop();
//     $('#test').html(scrollCount);
// 
// })