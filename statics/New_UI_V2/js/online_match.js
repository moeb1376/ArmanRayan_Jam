$("select[name='second-team']").change(function () {
    let id_selected = $(this).children("option:selected").val();
    if (id_selected == 1) {
        $("img[name='team2-img']").attr("src", unknownSrc);
        $("h4[name='team2-name']").text("تیم تصادفی");
        $("h5[name='team2-university']").text("");
    } else if (id_selected >= 2) {
        $("img[name='team2-img']").attr("src", armankadehLogoSrc);
        $("h4[name='team2-name']").text("هوش آرمانکده");
        if (id_selected == 2)
            $("h5[name='team2-university']").text("آسان");
        else if (id_selected == 3)
            $("h5[name='team2-university']").text("متوسط");
        else if (id_selected == 4)
            $("h5[name='team2-university']").text("سخت");
    }
});