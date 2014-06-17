//============================================================================
// CanvasWidget
//============================================================================

require(["widgets/js/widget"], function (WidgetManager) {

    // console.log('require widget_canvas.js');

    // Define the widget's View.
    var CanvasView = IPython.DOMWidgetView.extend({
        initialize: function (options) {
            // console.log('initialize');

            // Backbone model --> JavaScript
            this.model.on('change:src', this.update_src, this);
            this.model.on('change:transformation', this.update_transformation, this);
            // this.model.on('change:_height', this.update_height, this);
            // this.model.on('change:_width', this.update_width, this);

            CanvasView.__super__.initialize.apply(this, arguments);
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

            // Prevent text selection cursor on canvas when click dragging.
            // http://stackoverflow.com/questions/11805318/when-i-click-on-a-canvas-and-drag-my-mouse-the-cursor-changes-to-a-text-selecti
            this.canvas.onmousedown = function (event) {
                event.preventDefault();
            }

            // Prevent page from scroll with wheel events over canvas.
            this.canvas.onwheel = function (event) {
                event.preventDefault();
            }

            // Internal image element serving to render new image src data.  This object will
            // later be used as source data argument to the canvas' own `drawImage()` method.
            this.image = new Image();

            // Event handle for loading new data into the image element.
            var that = this
            var draw_image_onload = function () {
                that.draw(that.image);
            }

            this.image.onload = draw_image_onload

            // Draw content to the canvas if valid image data exists in the Backbone model.
            if (this.model.has('src')) {
                if (this.model.get('src') != '') {
                    this.update_src();
                }
            }

            // I noticed problems if this update() function call was left out, e.g. second views of
            // my model would not initially receive CSS style properties.
            this.update();
        },

        update_src: function () {
            // Model's `src`: Python --> JavaScript
            // console.log('update_src');

            // Copy image src from Backbone model to internal <img> element.
            this.image.src = this.model.get('src');
        },

        draw: function (image, xfrm) {
            // Draw image data from internal <img> to the <canvas>.
            // console.log('draw');

            var value
            value = image.height
            this.canvas.height = value
            this.canvas.style.height = value + 'px'
            this.model.set('_height', value);

            value = image.width
            this.canvas.width = value
            this.canvas.style.width = value + 'px'
            this.model.set('_width', value);

            // Draw image to screen and apply transform.
            this.context.drawImage(image, 0, 0);

            // Must call this.touch() after any modifications to Backbone Model data.
            this.touch();
        },

        update_transformation: function () {
            // Model's `transformation`: Python --> JavaScript
            console.log('update_transformation');

            // Apply new transformation.
            var M = this.model.get('transformation');
            console.log(M);
        },

        /////////////////////////////////////////////
        // JavaScript --> Python
        // Tell Backbone how to respond to JavaScript-generated events.
        //
        // Great reference for JavaScript events:
        // https://developer.mozilla.org/en-US/docs/Web/Reference/Events
        events: {
            'mousemove': 'handle_mouse',
            'mouseup': 'handle_mouse',
            'mousedown': 'handle_mouse',
            'wheel': 'handle_mouse',
            //  'click':      'handle_click',
            //  'mouseenter': 'handle_mouse',  // don't worry about these other mouse
            //  'mouseleave': 'handle_mouse',  // events for now.
            //  'mouseout':   'handle_mouse',
            //  'mouseover':  'handle_mouse',
        },

        // Extract information about a mouse event.
        // https://developer.mozilla.org/en-US/docs/Web/Reference/Events/mousemove
        _build_mouse_info: function (ev) {
            // http://stackoverflow.com/questions/17130395/canvas-html5-real-mouse-position
            // https://developer.mozilla.org/en-US/docs/Web/API/Element.getBoundingClientRect
            var rect = this.canvas.getBoundingClientRect();
            var x = parseInt(ev.clientX - rect.left);
            var y = parseInt(ev.clientY - rect.top);

            var info = {
                canvasX: x,
                canvasY: y,
            }

            // Copy select system mouse event attributes over to this application's mouse event
            // structure.
            var attr_basic = ['type', 'timeStamp', 'button',
                'ctrlKey', 'altKey', 'shiftKey', 'metaKey',
                'clientX', 'clientY'
            ]
            var key, ix
            for (ix in attr_basic) {
                key = attr_basic[ix]
                info[key] = ev[key]
            }

            // Check for `wheel` event.
            // https://developer.mozilla.org/en-US/docs/Web/Reference/Events/wheel
            var attr_wheel = ['deltaMode', 'deltaX', 'deltaY', 'deltaZ']
            if (info['type'] == 'wheel') {
                for (ix in attr_wheel) {
                    key = attr_wheel[ix]
                    info[key] = ev[key]
                }
            }

            return info
        },

        // Handle a mouse event.
        handle_mouse: function (jev) {
            var ev = jev.originalEvent
            // Event handler responding to mouse motion and button clicks.
            // console.log(ev);

            var info = this._build_mouse_info(ev)
            this.model.set('_mouse', info);

            // Must call this.touch() after any modifications to Backbone Model data.
            this.touch();
        },

        // // Handle mouse wheel scroll event.
        // handle_wheel: function (jev) {
        //     var ev = jev.originalEvent
        //     console.log(ev);
        //     console.log(ev.clientX);
        //     // this.model.set('_key', ev);
        //     // Must call this.touch() after any modifications to Backbone Model data.
        //     this.touch();
        // },
        // Handle keyboard event.
        // http://stackoverflow.com/questions/3729034/javascript-html5-capture-keycode-and-write-to-canvas
        // handle_keypress: function (ev) {
        //     console.log(ev);
        //     this.model.set('_key', ev);
        //     // Must call this.touch() after any modifications to Backbone Model data.
        //     this.touch();
        // }

    });

    // Register View with widget manager.
    // console.log('register');
    WidgetManager.register_widget_view('CanvasView', CanvasView);
});
