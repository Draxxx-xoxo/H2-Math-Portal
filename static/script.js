document.addEventListener('DOMContentLoaded', (event) => {
    // Check if we are on the target page
    if (document.getElementById('quiz')) {

        function checkServerTime() {
            fetch('http://computing.draxx.me/utilities/current_time')
                .then(response => response.json())
                .then(data => {
                    
                    let serverTime = new Date(data.current_time);
                    var time_remaining = targetTime - serverTime;
                    var days = Math.floor(time_remaining / (1000 * 60 * 60 * 24));
                    var hours = Math.floor((time_remaining % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
                    var minutes = Math.floor((time_remaining % (1000 * 60 * 60)) / (1000 * 60));
                    var seconds = Math.floor((time_remaining % (1000 * 60)) / 1000);

                    document.getElementById("countdown").innerHTML = days + "d " + hours + "h "
                    + minutes + "m " + seconds + "s ";

                    if (serverTime >= targetTime) {
                        window.location.assign(`https://computing.draxx.me/quiz/${quiz_id}/${session_id}/end`);
                        //window.location.assign(`http://localhost:3000/quiz/${quiz_id}/${session_id}/end`);
                    }
                })
                .catch(error => console.error('Error fetching server time:', error));
        }

        // Check the server time every second
        setInterval(checkServerTime, 1000);
    }
    else if(document.getElementById('add_quiz')){
        var limit = 5;
        $('input[type="checkbox"]').on('change', function(evt) {
            if ($('input[type="checkbox"]:checked').length > limit) {
                this.checked = false;
            }
        });
    }    
});

function showResetForm() {
    document.getElementById('login-form').style.display = 'none';
    document.getElementById('reset-form').style.display = 'block';
}
    
    // Function to show the login form
function showLoginForm() {
    document.getElementById('login-form').style.display = 'block';
    document.getElementById('reset-form').style.display = 'none';
}

async function generatecode() {
    var code = "";
    var possible = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";

    for (var i = 0; i < 6; i++)
        code += possible.charAt(Math.floor(Math.random() * possible.length));


    const response = await fetch('http://localhost:3000/utilities/insert_code', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },

        body: JSON.stringify({"code": code})

    });

    if (response.ok) {
        console.log('Code sent successfully');
    } else {
        console.error('Error sending code');
    }

    document.getElementById('classcode').innerHTML = code;

    document.getElementById('generatecode').style.display = 'none';
    document.getElementById('deletecode').style.display = 'block';
}

async function deletecode() {
    var code = document.getElementById("classcode").innerHTML;

    const response = await fetch('http://localhost:3000/utilities/delete_code', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },

        body: JSON.stringify({"code": code})

    });


    if (response.ok) {
        console.log('Code sent successfully');
    } else {
        console.error('Error sending code');
    }
    
    document.getElementById('classcode').innerHTML = '';
    document.getElementById('deletecode').style.display = 'none';
    document.getElementById('generatecode').style.display = 'block';
}

