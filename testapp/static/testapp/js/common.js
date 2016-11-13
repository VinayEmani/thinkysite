var common = {
    getTimeDescription: function(unixtime) {
        var SECOND = 1000;
        var MINUTE = SECOND * 60;
        var HOUR = MINUTE * 60;
        var DAY = HOUR * 24;
        var WEEK = DAY * 7;
        var MONTH = DAY * 30;
        var YEAR = 365 * DAY;

        var now = new Date().getTime();
        if (unixtime > now)
            // Likely, a bug some where.
            return "In future";

        var secondsPassed = (now - unixtime) ;

        if (secondsPassed <= 5 * SECOND)
            return "Just now";
        else if (secondsPassed >= 2 * YEAR)
            return Math.floor(secondsPassed / YEAR) + " years ago";
        else {
            var timeUnits  = [SECOND, MINUTE, HOUR, DAY, WEEK, MONTH, YEAR, 2 * YEAR];
            var timeUnitStrings = ["second", "minute", "hour", "day", "week", 
                "month", "year"];

            for (var i = 0;i < timeUnits.length - 1; i++) {
                if (secondsPassed >= timeUnits[i] && secondsPassed < timeUnits[i + 1])
                    if (secondsPassed < 2 * timeUnits[i])
                        return "a " + timeUnitStrings[i] + " ago";
                    else return Math.floor(secondsPassed / timeUnits[i]) + " " + timeUnitStrings[i] + "s ago";
            }

            return "Unknown time ago";
        }
    },

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

    setTimeTooltip: function() {
        $(".unixtime").each(function(i, e) {
            $(e).mouseenter(function(event) {
                unixtime = 1000 * Math.floor($(this).attr("value"));
                $(e).attr("title", common.getTimeDescription(unixtime));
            });
        })
    },
}
