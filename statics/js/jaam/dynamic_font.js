$(function () {
    let len_fit = 10; // According to your question, 10 letters can fit in.
    let un = $('#username');
    // Get the lenght of user name.
    let len_user_name = un.html().trim().length;
    if (len_fit < len_user_name) {
        // Calculate the new font size.
        let size_now = parseInt(un.css("font-size"));
        let size_new = size_now * len_fit / len_user_name;
        // Set the new font size to the user name.
        un.css("font-size", size_new);
    }
});