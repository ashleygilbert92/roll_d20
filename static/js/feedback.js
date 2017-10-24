$(document).ready(function () {
    $("#feedback_form").submit(function (event) {
        event.preventDefault();
        var campaign_name = $(this).find('option:selected').attr('id');
        // var campaign_owner = $(this).find('option:selected').attr('class');
        var player_name = $('#player_name').val();
        var date = $('#date').val();
        var feedback = $('#feedback').val();
        $.ajax({
            url: '/submit_feedback/',
            data: {
                'campaign_name': campaign_name,
                'player_name': player_name,
                'date': date,
                'feedback': feedback
            },
            type: 'POST',
            success: function (response) {
                $('#feedback_form')[0].reset();
                alert("SUCCESS! We received your feedback! Thanks!");
            },
            error: function (error) {
                console.log(error);
                alert("Something weird happened while adding your feedback. Make sure you input all fields correctly")
            }
        });
    });
});