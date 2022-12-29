document.getElementById("menu_type--bestmenu").innerText = $.getUrlVar('age')+"'s" + "에 추천";
if ($.getUrlVar('confidence') >= 0.5){
    $("#alert_for_low_confidence").hide();
}