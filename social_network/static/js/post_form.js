$(document).ready(function () {
    $('#id_media_form').hide();  // Hide the media form initially

    $('.fa-camera').click(function () {
        $('#id_media_form').toggle();  // Show/hide the media form when the camera icon is clicked
    });
});
