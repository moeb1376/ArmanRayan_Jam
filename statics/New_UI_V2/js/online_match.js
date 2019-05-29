$("select[name='second-team']").change(function () {
    console.log("jquery salam")
    let id_selected = $(this).children("option:selected").val();
    if (id_selected == 1){
        $("img[name='team2-img']").attr("src","../img/unknown.jpg");
        $("h4[name='team2-name']").text("تیم تصادفی");
        $("h5[name='team2-university']").text("");
    }
    else if (id_selected >=2){
        $("img[name='team2-img']").attr("src","../img/Armankadeh_logo_300.png");
        $("h4[name='team2-name']").text("هوش آرمانکده");
        if (id_selected == 2)
            $("h5[name='team2-university']").text("آسان");
        else if (id_selected == 3)
            $("h5[name='team2-university']").text("متوسط");
        else if (id_selected == 4)
            $("h5[name='team2-university']").text("سخت");
    }
});