function set_random_team_data(data) {
    if (data.status) {
        if (data.status == "Failed") {
            msg1 = 'شما یک بازی در حال اجرا دارید.';
            msg2 = 'لطفا تا پایان آن صبر کنید و دوباره تلاش کنید.';
            popup_show(msg1, msg2)
        }
    }
    else {
        document.getElementById("h2_team2_name").innerText = data.team_name;
        document.getElementById("university_small").innerText = data.university;
        document.getElementById("image_team2").setAttribute("src", data.image_url);
        document.getElementById("game_state").innerHTML = data.random_loading;
    }
}

function random_loading(data) {
    if (data.status) {
        // if (data.status == "Failed") {
        //     msg1 = 'شما یک بازی در حال اجرا دارید.';
        //     msg2 = 'لطفا تا پایان آن صبر کنید و دوباره تلاش کنید. می‌توانید نتیجه آن باز را در صفحه نتایج خو ببینید.';
        //     popup_show(msg1, msg2)
        // }
    }
    else {
        document.getElementById("game_state").innerHTML = data.random_loading
    }

}

function ajax_team_data() {
    var team1 = document.getElementById("team1_select_list");
    var team_selected_code = $("#team1_select_list").find("option:selected").text();
    if (team1.options.length > 0) {
        var e = document.getElementById("team2_select_list");
        if (e[e.selectedIndex].value === '2') {
            $.ajax({
                url: '/play_online_ajax/',
                data: {
                    'play': 2,
                    'team_selected_code': team_selected_code
                },
                dataType: 'json',
                success: set_random_team_data
            });
        }
        else {
            $.ajax({
                url: '/play_online_ajax/',
                data: {
                    'play': 1,
                    'team_selected_code': team_selected_code
                },
                dataType: 'json',
                success: random_loading
            });
        }
    }
    else {
        var start = document.getElementsByName("start-btn");
        msg1 = 'کدی برای تیم شما در سامانه ثبت نشده است';
        msg2 = 'اگر کد خود را آپلود کرده‌اید منتظر تایید آن باشید. <br> در غیر این صورت،لطفا برای شرکت در این بخش کد خود را در صفحه اصلی آپلود کنید.';
        start.onclick(popup_show(msg1, msg2));
    }
    msg1 = 'بازی در حال اجراست';
    msg2 = 'جهت اطلاع از نتیجه بازی به صفحه نتایج مراجعه کنید.';
    popup_show(msg1, msg2);
    var start_link = document.getElementById("start-link");
    start_link.removeAttribute("onclick");
    start_link.removeAttribute("href");
    var start_box = document.getElementById('start-box');
    start_box.setAttribute("class", "widget p-lg text-center");
    start_box.style.backgroundColor = "#5e5e5e";
}

function set_team2_data() {
    e = document.getElementById("team2_select_list");
    if (e[e.selectedIndex].value == "1") {
        document.getElementById("h2_team2_name").innerText = "آرمانکده";
        document.getElementById("university_small").innerText = "شرکت آرمان رایان شریف";
        document.getElementById("image_team2").setAttribute("src", "/statics/img/armankadeh.png");
    }
    else {
        document.getElementById("h2_team2_name").innerText = "تصادفی";
        document.getElementById("university_small").innerText = "";
        document.getElementById("image_team2").setAttribute("src", "/statics/img/unknown.jpg");
    }
}

function popup_show(msg1, msg2) {
    toastr.options = {
        closeButton: true,
        progressBar: true,
        showMethod: 'slideDown',
        timeOut: 7000,
        positionClass: "toast-top-center",
    };
    // var str = 'کدی برای تیم شما در سامانه ثبت نشده است';
    var result = msg1.fontsize(5);
    // var str1 = 'لطفا برای شرکت در این بخش کد خود را در صفحه اصلی آپلود کنید';
    var res1 = msg2.fontsize(3);
    toastr.info(res1, result);
}