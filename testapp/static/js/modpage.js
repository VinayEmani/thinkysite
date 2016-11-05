function updateMods(form_field_id, url, data_key) {
    return function(e) {
        e.preventDefault();
        // Ideally, we need to read this from cookie.
        var csrftoken = $("#add-mod-form")[0].children[0].value;
        var modname  = $(form_field_id)[0].value;
        $.ajax({
            "type": "POST",
            "url": url,
            "data": {
                data_key: modname
            },
            beforeSend: function(req) {
                req.setRequestHeader('X-CSRFToken', csrftoken);
            },
            success: function(data) {
                alert(data);
            },

            error: function(req, status, error) {
                alert(req.responseText);
            },
        });;
    }
};

window.onload = function() {
    $("#add-mod-button")[0].submit(
            updateMods("#add-mod-field", "/testapp/addnewmod/", "newmod"));
    $("#del-mod-button")[0].submit(
            updateMods("#del-mod-field", "/testapp/deloldmod/", "oldmod"));
};
