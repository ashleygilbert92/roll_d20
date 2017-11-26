$(document).ready(function () {
    $("#sign_up_form").submit(function (event) {
        event.preventDefault();
        var full_name = $('#full_name').val();
        var username = $('#username').val();
        var password = $('#password').val();
        $.ajax({
            url: '/add_user/',
            data: {
                'full_name': full_name,
                'username': username,
                'password': password
            },

            type: 'POST',
            success: function (response) {
                window.location.href = response["next"];
            },
            error: function (error) {
                console.log(error);
                alert("Something went wrong while signing you up! Please check all fields again.")
            }
        });
    });
});