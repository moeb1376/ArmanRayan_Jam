$("#send-key").click(function () {
    let user_id = $("#user-id").text();
    $.ajax({
        'url': '/api/get-key',
        data: {
            "user": user_id,
            "cup": 1
        },
        dataType: 'json',
        success: send_key_success_function,
        method: "GET"
    })
});

function send_key_success_function(data) {
    set_msg(data.msg);
    instance.open();
}

function set_msg(msg) {
    let modal_msg = $("#modal-text-msg");
    console.log(modal_msg);
    modal_msg.text(msg);
}