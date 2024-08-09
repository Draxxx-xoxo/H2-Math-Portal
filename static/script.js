document.addEventListener('DOMContentLoaded', (event) => {
    // Check if we are on the target page
    if (document.getElementById('quiz')) {

        function checkServerTime() {
            fetch('http://localhost:3000/utilities/current_time')
                .then(response => response.json())
                .then(data => {
                    
                    let serverTime = new Date(data.current_time); // 'Z' indicates UTC time
                    if (serverTime >= targetTime) {
                        window.location.assign("http://localhost:3000/dashboard");
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