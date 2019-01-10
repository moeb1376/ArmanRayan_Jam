$(document).ready(function () {
    let path = document.location.pathname;
    if (path.includes("new_jaam")) {
        $("#team_detail_item").addClass("icon-active");
        $("#team_detail_mobile_item").addClass("icon-active");
    } else if (path.includes("jaam_table")) {
        $("#table_jaam_item").addClass("icon-active");
        $("#table_jaam_mobile_item").addClass("icon-active");
    } else if (path.includes("table")) {
        $("#cup_item").addClass("icon-active");
        $("#cup_mobile_item").addClass("icon-active");
    }
});