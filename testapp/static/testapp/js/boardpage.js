$(document).ready(function () {
    $("#add-forum-options").hide();
    $("#add-forum-button").on("click", function() {
        $("#add-forum-options").toggle();
    });

    $("#add-forum-submit").on("click", function(event) {
        event.preventDefault();

        var fname = $("#add-forum-name").val();
        $("#add-forum-name").val("");
        var fdesc = $("#add-forum-desc").val();
        $("#add-forum-desc").val("");
        if (fname.length == 0 || fdesc.length == 0) {
            alert("Forum name and description can't be empty.");
            return;
        }

        // Fire up an ajax request.
        $.ajax({
            type: "POST",
            url: "/testapp/mod/forum/",
            dataType: "json",
            data: {
                action: "create",
                // Assumes the location isn't tampered with.
                boardid: common.getQueryParam("boardid"),
                name: fname,
                desc: fdesc
            },

            beforeSend: function(xhr) {
                xhr.setRequestHeader("X-CSRFToken", common.getCSRFToken());
            },

            success: function(data, status, xhr) {
                if (data.retCode == 0) {
                    // Simply reload page for now.
                    location.reload();
                } else {
                    alert(data.explanation);
                }
            }
        });
    })
});
