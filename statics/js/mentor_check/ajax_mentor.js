function ajax_mentor() {
    var d = document.getElementById('id_mentor').value;
    if (d.length < 3) {
        return false;
    }
    else if (d.length < 6) {
        change_mentor_icon({"find_mentor": false});
        return false;
    }
    $.ajax({
        url: '/mentor_ajax/',
        data: {
            'mentor_code': d
        },
        dataType: 'json',
        success: change_mentor_icon
    });

}

function change_mentor_icon(data) {
    var mentor_span = document.getElementById('id_mentor');
    // document.getElementById('div-mentor-icon-span').removeAttribute("hidden");
    if (data.find_mentor) {
        mentor_span.style['border-color'] = 'green';
    }
    else {
        mentor_span.style['border-color'] = 'red';
    }

}