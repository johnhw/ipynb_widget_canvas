(function ($) {
    console.log('init.js');

    // Synchronous script loader, assumes jQuery has already been loaded.
    // http://stackoverflow.com/a/7352694/282840
    function load_script(script_url) {
        $.ajax({
            url: script_url,
            dataType: 'script',
            async: false, //    <-- This is the key for async vs. sync
            cache: false,

            success: function () {
                var msg = 'Success loading: ' + script_url
                console.log(msg);
            },

            error: function (a, b, c) {
                console.log(a);
                console.log(b); // why did I put these here???
                console.log(c);

                var msg = 'Error loading: ' + script_url
                console.log(msg);
                throw new Error(msg);
            },
        });
    }

    /////////////////////////////////////////////
    // Load my application modules.

    // nb_canvas.js
    var url = 'nb_video/js/nb_video.js'
    load_script(url);

    if (typeof window.nbv === 'undefined') {
        var msg = 'Problem while loading: ' + url
        throw new Error(msg);
    }

})(jQuery);
