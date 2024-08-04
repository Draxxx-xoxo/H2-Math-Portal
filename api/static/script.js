var limit = 5;
$('input[type="checkbox"]').on('change', function(evt) {
    if ($('input[type="checkbox"]:checked').length > limit) {
        this.checked = false;
    }
});