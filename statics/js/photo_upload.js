$(function () {

    $(".js-upload-photos").click(function () {
        $("#fileupload").click();
    });

    $("#fileupload").fileupload({
        dataType: 'json',
        sequentialUploads: true, /* 1. SEND THE FILES ONE BY ONE */
        start: function (e) {  /* 2. WHEN THE UPLOADING PROCESS STARTS, SHOW THE MODAL */
            $("#modal-progress").modal("show");
        },
        stop: function (e) {  /* 3. WHEN THE UPLOADING PROCESS FINALIZE, HIDE THE MODAL */
            $("#modal-progress").modal("hide");
            alert("بارگذاری با موفقیت انجام شد")
        },
        progressall: function (e, data) {  /* 4. UPDATE THE PROGRESS BAR */
            var progress = parseInt(data.loaded / data.total * 100, 10);
            var strProgress = progress + "%";
            // $(".progress-bar").css({"width": strProgress});
            var progress_bar = $("#upload_progress_bar");
            progress_bar.css({"width": strProgress});
            // $(".progress-bar").text(strProgress);
            progress_bar.text(strProgress);
        },
        done: function (e, data) {
        }

    });

});