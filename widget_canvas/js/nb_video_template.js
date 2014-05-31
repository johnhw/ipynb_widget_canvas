
// app.js
define(['video-js/video'],
function(vjs) {
    console.log('define nb_video_app');

    var parameters = {vjs: vjs}

    // Application logic is determined by the functions contained within this object literal.
    var app = {
        init: function(config) {
            // This function initializes stuff.
            console.log('app init');


            parameters.id_video = config.id_video;
            parameters.url = null;

            var config_vjs = {}

            var el = document.getElementById(parameters.id_video);

            parameters.vjs(el, config_vjs, this.just_a_callback);
        },

        just_a_callback: function() {
            // Placeholder.
        },

        do_something: function() {
            // Do some work.
            console.log('app do_something')

            console.log(parameters)
        },
    }

    // Return the ready-to-use app.
    return app;2
});


var nb_video = (function() {
    var vjs =
    var init = function() {

    }


})();


//
// Example Module Pattern
// http://javascriptplayground.com/blog/2012/04/javascript-module-pattern/
//
// var jspy = (function() {
//   var _count = 0;
//   var incrementCount = function() {
//     _count++;
//   };
//   var resetCount = function() {
//     _count = 0;
//   };
//   var getCount = function() {
//     return _count;
//   };
//   return {
//     add: incrementCount,
//     reset: resetCount,
//     get: getCount
//   };
// })();
//
