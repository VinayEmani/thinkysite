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
        // TODO(vinay) :- Ideally, should read this from cookie.
        var csrftoken = $("#add-mod-form")[0].children[0].value;
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

$(document).ready(function() {
    $("#add-mod-form").submit(
            updateMods("#add-mod-field", "/testapp/addnewmod/", "newmod"));
    $("#del-mod-form").submit(
            updateMods("#del-mod-field", "/testapp/deloldmod/", "oldmod"));

    $("#add-board-options").hide();
    $("#add-board-button").on("click", function(event) {
        $("#add-board-options").toggle();
    });

    $("#add-board-submit").on("click", function(event) {
        event.preventDefault();

        // Fire an ajax request.
    });
});
