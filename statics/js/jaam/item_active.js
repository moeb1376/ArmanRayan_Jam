$(document).ready(function () {
    let path = document.location.pathname;
    if (path.match("jaam/$") ) {
        $("#team_detail_item").addClass("icon-active");
        $("#team_detail_mobile_item").addClass("icon-active");
    } else if (path.match("jaam_tables/$")) {
        $("#table_jaam_item").addClass("icon-active");
        $("#table_jaam_mobile_item").addClass("icon-active");
    } else if (path.match("table/$")) {
        $("#cup_item").addClass("icon-active");
        $("#cup_mobile_item").addClass("icon-active");
    } else if (path.match("play/$")) {
        $("#friendly_item").addClass("icon-active");
        $("#friendly_mobile_item").addClass("icon-active");
    } else if (path.match("log/$")) {
        $("#log_item").addClass("icon-active");
        $("#log_mobile_item").addClass("icon-active");
    } else if (path.match("setting/$")) {
        $("#setting_item").addClass("icon-active");
    }
});