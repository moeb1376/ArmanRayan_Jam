function get_validate(form_id) {
    if (validate()) {
        document.getElementById(form_id).submit();
    }
}

function validate() {
    var v = grecaptcha.getResponse();
    if (v.length == 0) {
        // document.getElementById('captcha').innerHTML = "You can't leave Captcha Code empty";
        // alert("You can't leave Captcha Code empty");
        add_alert();
        return false;
    }
    else {
        return true;
    }
}

function add_alert() {
    var alert_box = document.getElementById('Alert-box');
    if (alert_box) {
        alert_box.removeAttribute('hidden');
        document.getElementById('alert-msg').innerHTML = "Enter reCaptcha!";
    }
    else {
        alert_box = document.createElement('div');
        alert_box.setAttribute("class","alert alert-danger alert-dismissible");
        alert_box.setAttribute("id", "Alert-box");
        var a = document.createElement('a');
        a.setAttribute("class","close");
        a.setAttribute("href", "#");
        a.setAttribute("data-dismiss", "alert");
        a.setAttribute("aria-label", "close");
        a.innerHTML = "&times;";
        var msg = document.createElement('p');
        msg.innerHTML = "Enter reCaptcha";
        alert_box.appendChild(a);
        alert_box.appendChild(msg);
        var p = document.getElementById("recaptcha");
        p.parentNode.insertBefore(alert_box,p.nextSibling);
    }
}