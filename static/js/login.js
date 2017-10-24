$(document).ready(function () {
    $("#login_form").submit(function (event) {
        event.preventDefault();
        var username = $('#username').val();
        var password = $('#password').val();
        $.ajax({
            url: '/authenticate/',
            data: {
                'username': username,
                'password': password
            },

            type: 'POST',
            success: function (response) {
                window.location.href = response["next"];
            },
            error: function (error) {
                console.log(error);
                alert("Email or Password was invalid")
            }
        });
    });
});