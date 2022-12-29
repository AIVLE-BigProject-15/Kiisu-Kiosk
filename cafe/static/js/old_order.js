document.getElementById("menu_type--bestmenu").innerText = "BEST FOR " + $.getUrlVar('age')+"'s";
if ($.getUrlVar('confidence') >= 0.5){
    $("#alert_for_low_confidence").hide();
}