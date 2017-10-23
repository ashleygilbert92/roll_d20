$(document).ready(function () {
    $("#login_form").submit(function (event) {
        event.preventDefault();
        $.ajax({
            url: '/authenticate/',
            data: $('#login_form').serialize(),
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
