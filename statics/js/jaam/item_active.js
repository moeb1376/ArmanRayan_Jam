$(document).ready(function () {
    let path = document.location.pathname;
    let mobile_item
    console.log(path.match("index/$"));
    if (path.match("index/$")) {
        $("#team_detail_item").addClass("icon-active");
        mobile_item = $("#team_detail_mobile_item");
        mobile_item.addClass("icon-active");
        mobile_item.parent("a").addClass("sidenav_field_active");
    } else if (path.match("cup_tables/$")) {
        $("#table_jaam_item").addClass("icon-active");
        mobile_item = $("#table_jaam_mobile_item");
        mobile_item.addClass("icon-active");
        mobile_item.parent("a").addClass("sidenav_field_active");
    } else if (path.match("table/$")) {
        $("#cup_item").addClass("icon-active");
        mobile_item = $("#cup_mobile_item");
        mobile_item.addClass("icon-active");
        mobile_item.parent("a").addClass("sidenav_field_active")
    } else if (path.match("play/$")) {
        $("#friendly_item").addClass("icon-active");
        mobile_item = $("#friendly_mobile_item");
        mobile_item.addClass("icon-active");
        mobile_item.parent("a").addClass("sidenav_field_active")
    } else if (path.match("log/$")) {
        $("#log_item").addClass("icon-active");
        mobile_item = $("#log_mobile_item");
        mobile_item.addClass("icon-active");
        mobile_item.parent("a").addClass("sidenav_field_active")
    } else if (path.match("setting[0-9]/$")) {
        $("#team_setting_item").addClass("icon-active");
        mobile_item =$("#team_setting_mobile_item");
        mobile_item.addClass("icon-active");
        mobile_item.parent("a").addClass("sidenav_field_active")
    }
});