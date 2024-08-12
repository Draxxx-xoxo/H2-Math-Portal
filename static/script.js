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
                        window.location.assign("http://computing.draxx.me/dashboard");
                        // window.location.assign("http://localhost:3000/quiz/submit") // Future implementation
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