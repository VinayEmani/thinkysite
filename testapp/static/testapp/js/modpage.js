function getCSRFToken() {
    return $("[name=csrfmiddlewaretoken]").val();
}

function loadModList() {
    // Send a http request to /testapp/curmodlist and get all the mod list.
    $.ajax({
        "type": "GET",
        "url": "/testapp/curmodlist/",
        "async": "false",
        "success": function(data) {
            var mod_list_elem = $("#cur-mod-list")[0];
            while (mod_list_elem.hasChildNodes())
                mod_list_elem.removeChild(mod_list_elem.lastChild);

            for (var e in data) {
                var elem = document.createElement("a");
                elem.href = "/testapp/profile/?pid=" + data[e];
                elem.innerHTML = "<b><u> " + e + " </u></b>";
                mod_list_elem.appendChild(elem);
            }
         },
        "error": function(xhr) {
        }
    });
}

function updateMods(form_field_id, url, data_key) {
    return function(e) {
        e.preventDefault();
        var csrfToken = getCSRFToken();
        var modname  = $(form_field_id)[0].value;
        $(form_field_id)[0].value = "";
        var data = {};
        data[data_key] = modname;
        $.ajax({
            "type": "POST",
            "url": url,
            "data": data,
            beforeSend: function(req) {
                req.setRequestHeader('X-CSRFToken', csrftoken);
            },

            success: function(data) {
                loadModList();
            },

            error: function(req, status, error) {
                alert(req.responseText);
            },
        });;
    }
};

function loadBoardList() {
    return $.ajax({
        async: false,
        url: "/testapp/boardlist/",
        type: "GET",
        dataType: "json",
        success: function (data, status, xhr) {
            var fragment = document.createDocumentFragment();
            for (var id in data) {
                var name = data[id].name;
                var desc = data[id].desc;

                var outerDiv = document.createElement("div");
                $(outerDiv).addClass("row").css("border", "solid blue 1px");
                var leftDiv = document.createElement("div");
                $(leftDiv).addClass("col-lg-4");
                var html = "<b><a href=\"/testapp/board/?boardid=" + 
                        id.toString() + "\">" + name + "</a></b><br>";
                html += "<p>" + desc + "</p>";
                leftDiv.innerHTML = html;
                var rightDiv = document.createElement("div");
                $(rightDiv).addClass("col-lg-8");
                outerDiv.appendChild(leftDiv);
                outerDiv.appendChild(rightDiv);
                fragment.appendChild(outerDiv);
            }

            $("#board-list-div").empty();
            $("#board-list-div").append(fragment);
        },

        error: function(data, status, xhr) {
        }
    });
}

$(document).ready(function() {
    $("#add-mod-form").submit(
            updateMods("#add-mod-field", "/testapp/addnewmod/", "newmod"));
    $("#del-mod-form").submit(
            updateMods("#del-mod-field", "/testapp/deloldmod/", "oldmod"));

    $("#add-board-options").hide();
    $("#add-board-button").on("click", function(event) {
        $("#add-board-options").toggle();
        if ($("#add-board-options").is(":visible"))
            window.location.hash = "#add-board-options";
    });

    $("#add-board-submit").on("click", function(event) {
        event.preventDefault();
        var boardname = $("#add-board-name").val();
        var boarddesc = $("#add-board-desc").val();
        $("#add-board-name").val("");
        $("#add-board-desc").val("");

        if (boardname.length === 0 || boarddesc.length === 0) {
            alert("Name or description can't be empty.");
            return;
        }

        $.ajax({
            type: "POST",
            url: "/testapp/mod/board/",
            dataType: "json",
            data: {
                "action": "create",
                "boardname": boardname,
                "boarddesc": boarddesc,
            },
            beforeSend: function(xhr) {
                xhr.setRequestHeader("X-CSRFToken", getCSRFToken());
            },

            success: function (data, status, jqXHR) {
                if (data.retCode != 0) {
                    alert(data.explanation);
                    return;
                }

                alert("Successfully added a new board.");
                loadBoardList();
            },

            error: function(data, status, jqXHR) {
                alert("Something went wrong.");
                alert(data.explanation);
            },
        });
    });
});
