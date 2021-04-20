$(document).ready(function() {
    $("#right-list-inner li > h4").click(function() {

        if ($(this).next().is(':visible')) {
            $(this).next().slideUp();
            $(this).children(".plusminus").text('+');
        } else {
            $(this).next("#right-list-inner ul").slideDown();
            $(this).children(".plusminus").text('-');
        }
    });
});