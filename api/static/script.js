document.addEventListener('DOMContentLoaded', (event) => {
    // Check if we are on the target page
    if (document.getElementById('quiz')) {

        let targetTime = new Date();
        targetTime.setMinutes(targetTime.getMinutes() + 5);

        function checkServerTime() {
            fetch('http://localhost:3000/utilities/current_time')
                .then(response => response.json())
                .then(data => {
                    
                    let serverTime = new Date(data.current_time + 'Z'); // 'Z' indicates UTC time
                    console.log('Server time:', serverTime);
                    console.log("Target time:", targetTime)
                    if (serverTime >= targetTime) {
                        // Needs updating
                        // If the server time is equal to or greater than the target time, redirect
                        //window.location.href = 'https://www.example.com'; // Replace with your target URL
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