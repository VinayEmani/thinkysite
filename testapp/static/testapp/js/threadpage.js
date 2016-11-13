function editComment(event) {
    var jqe = $(this);
    event.preventDefault();
    console.log("edit clicked");
    var row = jqe.closest(".commentrow");
    var commentId = row.attr("id");

    if (commentId == undefined) {
        console.log("Comment id not set.");
        return;
    }
}

$(document).ready(function () {
    common.setTimeTooltip();
    $(".editcomment").on("click", editComment);
    // $(".deletecomment").on("click", deleteComment);
    // $(".upvotecomment").on("click", upvoteComment);
    // $(".downvoteComment").on("click", downvoteComment);
});
