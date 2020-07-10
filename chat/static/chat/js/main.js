$("#profile-img").click(function () {
    $("#status-options").toggleClass("active");
});

$(".expand-button").click(function () {
    $("#profile").toggleClass("expanded");
    $("#contacts").toggleClass("expanded");
});

$('.messages').stop().animate({
    scrollTop: $('.messages')[0].scrollHeight
}, 800);

function scroll() {
    $('.messages').stop().animate({
        scrollTop: $('.messages')[0].scrollHeight
    }, 800);
}

function scroll_up() {
    $('.messages').animate({ scrollTop: 0 }, 'fast');
}

$('.submit').click(function () {
    scroll();
});

$('#check_older_messages').click(function () {
    scroll_up();
});