
function main_init() {

    // Video element
    // https://developer.mozilla.org/en-US/docs/Web/API/HTMLMediaElement
    // https://developer.mozilla.org/en-US/docs/Web/API/HTMLVideoElement
    var el_video = $('#video_display')[0];
    var el_play_button = $('#play_button')[0];

    // var position = $('#position');
    // var using = $('#using');
    // var controls = $('#player_controls');

    // Event handlers.
    function handle_test_click(ev) {
        console.log('handle_test_click');
        // console.log(ev);

        $('#current_time').val(el_video.currentTime);

        // console.log(el_video);
        // console.log(el_video.videoWidth);
        // console.log(el_video.duration);
        // console.log(el_video.NETWORK_NO_SOURCE);
    }


    function console_status(ev) {
        console.log('console_status');

        console.log(el_video.networkState);
        console.log(el_video.playbackRate);
        console.log(el_video.readyState);
        console.log(el_video.HAVE_ENOUGH_DATA);
        console.log(el_video.seekable);
        console.log(el_video.paused);
    }

    // Attach event handlers.
    // https://developer.mozilla.org/en-US/docs/Web/API/EventTarget.addEventListener
    // http://api.jquery.com/on/
    $('#video_display').on("loadedmetadata", init_ready);

    $('#test_button_A').on("click", handle_test_click);
    $('#test_button_B').on("click", console_status);

    /////////////////////////////////////////////

    // This function is called when all metadata is loaded and ready.
    // Assume all methods and properties are ready for action.
    function init_ready(ev) {
        console.log('init_ready')

        // Attach some callback functions.
        $('#play_button').on("click", handle_play_toggle);
        $('#video_display').on("timeupdate", handle_time_update);
    }


    function handle_play_toggle(ev) {
        // console.log('handle_play_toggle');
        if (el_video.paused) {
          el_video.play();
          el_play_button.value = "Pause";
        } else {
          el_video.pause();
          el_play_button.value = "Play";
        }
    }


    function handle_time_update(ev) {
        console.log('handle_time_update');
        // console.log(el_video);

        console.log(el_video.currentTime);

        var minutes = Math.floor(el_video.currentTime / 60.);
        var seconds = Math.round(el_video.currentTime % 60.);

        if (minutes < 10) {
            minutes = '0' + minutes;
        } else {
            minutes = '' + minutes;
        }

        if (seconds < 10) {
            seconds = '0' + seconds;
        } else {
            seconds = '' + seconds;
        }

        var nice_time = minutes + ':' + seconds;
        console.log(nice_time);
        $('#current_time').text(nice_time);
    }

}
