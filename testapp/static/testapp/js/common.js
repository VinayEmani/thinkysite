var common = {
    getCSRFToken: function() {
        return $("[name=csrfmiddlewaretoken]").val();
    },

    getQueryParam: function(param) {
        queryParts = window.location.search.substring(1).split("&");
        for (var part in queryParts) {
            var tokens = queryParts[part].split("=");
            if (tokens[0] == param)
                return tokens[1];
        }

        return "";
    },
}
