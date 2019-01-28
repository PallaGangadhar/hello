
$(document).ready( function() { $("#about-btn").click( function(event) {
    alert("You clicked the button using JQuery!");
});
});


$(document).ready( function() {
    $("p").hover( function() { 
        $(this).css('color', 'red');
        }, function() {
        $(this).css('color', 'blue'); 
    });
});

$(document).ready( function() {
    $("#about-btn1").click( function(event) { 
        msgstr = $("#msg").html()
        msgstr = msgstr + "ooo" 
        $("#msg").html(msgstr)
    });
});