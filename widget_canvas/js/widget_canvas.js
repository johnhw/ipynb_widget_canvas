//============================================================================
// CanvasWidget
//============================================================================
// console.log('module widget_canvas.js');

require([
    "widgets/js/widget",
    "jquery",
], function (WidgetManager, $) {

    // console.log('define widget_canvas.js');

    // Define the widget View.
    var CanvasImageBaseView = IPython.DOMWidgetView.extend({
        initialize: function (options) {
            // console.log('initialize');

            // Backbone Model --> My JavaScript View
            this.model.on('change:data_encode', this.update_data_encode, this);
            // this.model.on('change:width', this.update_width, this);
            // this.model.on('change:height', this.update_height, this);
            // this.model.on('change:_transform_values', this.update_transform, this);
            // this.model.on('change:smoothing', this.update_smoothing, this);

            // this.time_mouse = Date.now()
            // this.time_mouse_threshold = 20 // miliseconds
            CanvasImageBaseView.__super__.initialize.apply(this, arguments);
        },

        render: function () {
            // Render a widget's view instance to the DOM.
            // console.log('render');

            // This project's view is quite simple: just a single <canvas> element.
            // http://stackoverflow.com/questions/3729034/javascript-html5-capture-keycode-and-write-to-canvas
            this.setElement('<canvas />');

            // Gather some handy references for the canvas and its context.
            this.canvas = this.el
            this.context = this.canvas.getContext('2d');

            // Internal image element serving to render new image src data.  This object will
            // later be used as source data argument to the canvas' own `drawImage()` method.
            this.image = new Image();

            // Event handling for drawing new data to the canvas.
            var that = this
            var draw_onload = function () {
                // console.log('draw_onload');
                that.update_data_image();
            }

            this.image.onload = draw_onload

            // Does any valid data exist in the system?  Copy data_b64 if it exists in model.
            if (this.model.has('data_encode')) {
                // console.log('render has b64');
                if (this.model.get('data_encode') != '') {
                    // console.log('render has OK data_encode');
                    this.update_data_encode();
                }
            }

            // I noticed problems if this update() function call was left out, e.g. second views of
            // my model would not initially receive CSS style properties.
            this.update();
        },

        update_data_encode: function () {
            // Python --> JavaScript, copy new value from Backbone model, apply to this View.
            // console.log('update_data_encode');

            this.image.src = this.model.get('data_encode');

            // Event processing continues inside this.image's defined onload() event handler.
        },

        update_data_image: function () {
            // Helper handler.
            // console.log('update_data_image');

            this.set_width(this.image.width);
            this.set_height(this.image.height);

            this.draw();
        },

        update_width: function () {
            // Python --> JavaScript
            // console.log('update_width');
            this.set_width(this.model.get('width'));
            this.draw();
        },

        update_height: function () {
            // Python --> JavaScript
            // console.log('update_height');
            this.set_height(this.model.get('height'));
            this.draw();
        },

        set_width: function (value) {
            // console.log('set_width: ', value);

            this.canvas.width = value
            this.canvas.style.width = value + 'px'

            this.model.set('width', value);
            this.touch();
        },

        set_height: function (value) {
            // console.log('set_height: ', value);

            this.canvas.height = value
            this.canvas.style.height = value + 'px'

            this.model.set('height', value);
            this.touch()
        },

        clear: function () {
            // Clear the canvas while preserving current state.
            // http://stackoverflow.com/a/6722031/282840
            // console.log('clear: ', 0, 0, this.canvas.width, this.canvas.height);

            this.context.save();

            this.context.setTransform(1, 0, 0, 1, 0, 0);
            this.context.clearRect(0, 0, this.canvas.width, this.canvas.height);

            this.context.restore();
        },

        draw: function () {
            // Draw image data from internal <img> to the <canvas>.
            // console.log('draw');

            // Clear any prior image data.
            this.clear();
            // this.set_smoothing(false);

            // Draw image to screen.
            this.context.drawImage(this.image, 0, 0);

            // Must call this.touch() after any modifications to Backbone Model data.
            // this.touch();
        },
    });

    // Define the widget View.
    var CanvasImageFancyView = CanvasImageBaseView.extend({
        initialize: function (options) {
            console.log('initialize Fancy');

            // Backbone Model --> My JavaScript View
            // this.model.on('change:width', this.update_width, this);
            // this.model.on('change:height', this.update_height, this);
            // this.model.on('change:_transform_values', this.update_transform, this);
            this.model.on('change:smoothing', this.update_smoothing, this);

            CanvasImageFancyView.__super__.initialize.apply(this, arguments);
        },

        // render: function () {
        //     // Render a widget's view instance to the DOM.
        //     // console.log('render');

        //     // This project's view is quite simple: just a single <canvas> element.
        //     // http://stackoverflow.com/questions/3729034/javascript-html5-capture-keycode-and-write-to-canvas
        //     this.setElement('<canvas />');

        //     // Gather some handy references for the canvas and its context.
        //     this.canvas = this.el
        //     this.context = this.canvas.getContext('2d');

        //     // Internal image element serving to render new image src data.  This object will
        //     // later be used as source data argument to the canvas' own `drawImage()` method.
        //     this.image = new Image();

        //     // Event handling for drawing new data to the canvas.
        //     var that = this
        //     var draw_onload = function () {
        //         // console.log('draw_onload');
        //         that.update_data_image();
        //     }

        //     this.image.onload = draw_onload

        //     // Does any valid data exist in the system?  Copy data_b64 if it exists in model.
        //     if (this.model.has('data_encode')) {
        //         // console.log('render has b64');
        //         if (this.model.get('data_encode') != '') {
        //             // console.log('render has OK data_encode');
        //             this.update_data_encode();
        //         }
        //     }

        //     // I noticed problems if this update() function call was left out, e.g. second views of
        //     // my model would not initially receive CSS style properties.
        //     this.update();
        // },

        update_smoothing: function () {
            // Python --> JavaScript
            console.log('update_smoothing');
            this.set_smoothing(this.model.get('smoothing'));
        },

        set_smoothing: function (value) {
            this.context.mozImageSmoothingEnabled = value
            this.context.oImageSmoothingEnabled = value
            this.context.webkitImageSmoothingEnabled = value
            this.context.imageSmoothingEnabled = value
        },

    });

    // Register Views with widget manager.

    // Note: the method called below must be "register_widget_view", NOT "register_widget_model"!!
    console.log('register views');
    WidgetManager.register_widget_view('CanvasImageBaseView', CanvasImageBaseView);
    WidgetManager.register_widget_view('CanvasImageFancyView', CanvasImageFancyView);
});
