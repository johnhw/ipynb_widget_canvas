// self-executing anonymous function to setup a player constructor.
//http://markdalgleish.com/2011/03/self-executing-anonymous-functions/
(function ($) {
    console.log('nb_video.js');
    // console.log(this)

    var new_player = function (config_user) {
        // Function to build and return new player instance.
        console.log('build new_player')

        ////////////////////////////////////////

        // VideoJS options.
        // https://github.com/videojs/video.js/blob/master/docs/guides/options.md

        // Parameters initialized with default vales.
        var config = {
            id_video: 999,
            width: 200,
            height: 100,
            controls: true,
            autoplay: false,
            preload: 'auto',
        }

        // Update parameters with user-supplied values.
        for (var i in config_user) {
            config[i] = config_user[i]
        }

        // Event handler functions.
        var play = function () {
            console.log('play');
        }

        var stop = function () {
            console.log('stop!');
        }

        var seek = function (new_time) {
            console.log('seek');
        }

        var just_a_callback = function () {
            console.log('just_a_callback');
        }

        var another_callback = function (ev) {
            console.log('another_callback');
            console.log(ev);
        }

        // Tell VideoJS about my video element.
        video_el = document.getElementById(config.id_video)
        var _vjs_player = window.vjs(video_el, config, just_a_callback);

        // Modify VideoJS display & config settings.
        // http://api.jquery.com/class-selector/
        // http://api.jquery.com/css/
        // http://stackoverflow.com/a/16086227/282840     <-- nice

        // Hide the big play button at all times.
        $('.vjs-default-skin .vjs-big-play-button').css({
            'display': 'none',
        });

        // Shift control bar downwards.
        $('.vjs-default-skin .vjs-control-bar').css({
            'bottom': -39,
            'display': 'block',
        });

        // Display control bar at all times.
        $('.vjs-default-skin .vjs-has-started .vjs-user-inactive .vjs-playing .vjs-control-bar').css({
            'display': 'block', // 'none' to hide, 'block' to show ?????
            'visibility': 'visible',
        });

        // Remove full-screen button.
        // http://help.videojs.com/discussions/questions/12-is-it-possible-to-disableremove-full-screen-button
        // http://help.videojs.com/discussions/problems/975-option-for-removing-fullscreen-button
        $('.vjs-default-skin .vjs-fullscreen-control ').css({
            'display': 'none', // 'none' to hide, 'block' to show ?????
        });

        // Remove volume controls.
        $('.vjs-default-skin .vjs-volume-control').css({
            'display': 'none',
        });
        $('.vjs-default-skin .vjs-mute-control').css({
            'display': 'none',
        });

        /////////////////////////////////////////

        var player = {
            // _vjs_player: _vjs_player,
            play: play,
            stop: stop,
            seek: seek,
        }

        return player
    }

    // Place my builder function in global window namespace.
    window.nbv = {} // Note-Book-Video-Player

    window.nbv.new_player = new_player

})(jQuery);
