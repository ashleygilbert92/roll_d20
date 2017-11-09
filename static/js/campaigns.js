$(document).ready(function () {
    $("#submit_campaign").click(function (event) {
        event.preventDefault();
        var name = $('#name').val();
        $.ajax({
            url: '/add_campaign/',
            data: {
                'name': name
            },
            type: 'POST',
            success: function (response) {
                window.location.href = response["next"];
            },
            error: function (error) {
                console.log(error);
                alert("Something weird happened while adding your new campaign. Make sure you input all fields correctly")
            }
        });
    });
});