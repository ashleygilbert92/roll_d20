$(document).ready(function () {
    $("#averages_form").submit(function (event) {
        event.preventDefault();
        var roll = $('#roll').val();
        $.ajax({
            url: '/add_roll/',
            data: {
                'roll': roll
            },
            type: 'POST',
            success: function (response) {
                $('#today_average').replaceWith('<h4 class="card-title" id="today_average">'
                    + response['today_average'].toLocaleString() + '</h4>');
                $('#total_average').replaceWith('<h4 class="card-title" id="total_average">'
                    + response['total_average'].toLocaleString() + '</h4>');
            },
            error: function (error) {
                console.log(error);
                alert("Something weird happened while adding a new dice roll. Please Try again!")
            }
        });
    });
    $("#probability_form").submit(function (event) {
        event.preventDefault();
        var four = $('#4').val();
        var six = $('#6').val();
        var eight = $('#8').val();
        var ten = $('#10').val();
        var twelve = $('#12').val();
        var twenty = $('#20').val();
        var one_hundred = $('#100').val();
        var target = $('#target').val();
        $.ajax({
            url: '/calculate_probability/',
            data: {
                '4': four,
                '6': six,
                '8': eight,
                '10': ten,
                '12': twelve,
                '20': twenty,
                '100': one_hundred,
                'target': target
            },
            type: 'POST',
            success: function (response) {
                $('#probability_header').replaceWith('<h4 class="card-title" id="probability_header">' +
                    response['probability'].toLocaleString() + '&#37;</h4>');
            },
            error: function (error) {
                console.log(error);
                alert("Something weird happened while calculating probability. Please Try again!")
            }
        });
    });
});
