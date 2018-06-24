function add_team() {
    $.ajax({
        url: '/add_team_ajax/',
        data: {
            'add': true
        },
        method: "POST",
        dataType: 'json',
        success: function (data) {
            var add_btn = document.getElementById('add-team-btn');
            add_btn.style.backgroundColor = '#5e5e5e';
            add_btn.removeAttribute('onclick');
            window.location.reload(false);
        }
    });
}