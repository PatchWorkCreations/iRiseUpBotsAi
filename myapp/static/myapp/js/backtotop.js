$(document).ready(function() {
    console.log('Document is ready');
    var e = document.querySelector('.progress-wrap path');
    
    if (!e) {
        console.error('Element .progress-wrap path not found');
        return;
    }

    console.log('Element found');
    var t = e.getTotalLength();
    e.style.transition = e.style.WebkitTransition = 'none';
    e.style.strokeDasharray = t + ' ' + t;
    e.style.strokeDashoffset = t;
    e.getBoundingClientRect();
    e.style.transition = e.style.WebkitTransition = 'stroke-dashoffset 10ms linear';
    
    var o = function() {
        var o = $(window).scrollTop(),
            r = $(document).height() - $(window).height(),
            i = t - (o * t / r);
        e.style.strokeDashoffset = i;
    };

    o();
    $(window).scroll(o);

    jQuery(window).on('scroll', function() {
        jQuery(this).scrollTop() > 50 ? jQuery('.progress-wrap').addClass('active-progress') : jQuery('.progress-wrap').removeClass('active-progress');
    });

    jQuery('.progress-wrap').on('click', function(s) {
        s.preventDefault();
        jQuery('html, body').animate({scrollTop: 0}, 550);
        return false;
    });
});
