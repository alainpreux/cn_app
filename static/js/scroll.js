function windowSize(){
            var windowHeight = $(window).height() - $('#menutop').height();
            $('.section').css({
                minHeight : windowHeight
            })
        }
       
        $(window).resize(function(){
            windowSize()
        });
 $(document).ready(function(){
            windowSize();
            $('#header a').click(function(){
             
             $('.nav li').removeClass('active');
 $(this).parent('li').addClass('active');
                var pageId = $(this).attr('href');
                $('html, body').animate({
                    scrollTop: $(pageId).offset().top - $('#menutop').height()
                }, 500);
                return false
            })
            
            var scrollPos = $('.content #page2').offset().top();
   $('#page2').html(scrollPos);
   
        })
 $(window).scroll(function(){
    var scrollCount = $(window).scrollTop();
$('#test').html(scrollCount);
})