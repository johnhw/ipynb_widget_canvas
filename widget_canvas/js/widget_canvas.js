//============================================================================
// CanvasWidget
//============================================================================

require(["widgets/js/widget"], function (WidgetManager) {

    // console.log('require widget_canvas.js');

    // Define the widget's View.
    var CanvasView = IPython.DOMWidgetView.extend({
        initialize: function (options) {
            console.log('initialize');

            // Backbone Model --> My JavaScript View
            this.model.on('change:src', this.update_src, this);
            // this.model.on('change:width', this.update_width, this);
            // this.model.on('change:height', this.update_height, this);
            this.model.on('change:transformation', this.update_transformation, this);

            CanvasView.__super__.initialize.apply(this, arguments);
        },

        render: function () {
            // Render a widget's view instance to the DOM.
            console.log('render');

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

            // Prevent page from scrolling with mouse wheel events over canvas.
            this.canvas.onwheel = function (event) {
                event.preventDefault();
            }

            // Internal image element serving to render new image src data.  This object will
            // later be used as source data argument to the canvas' own `drawImage()` method.
            this.image = new Image();

            // Event handling for drawing new data to the canvas.
            // var that = this
            var that = this
            var draw_onload = function () {
                console.log('draw_onload');
                that.draw();
            }

            this.image.onload = draw_onload

            // Does any valid data exist in the system?
            // console.log('render width, height: ', this.image.width, this.image.height);
            if (this.image.width != 0 && this.image.height != 0) {
                // Force a call to this.draw() if valid data exists in the internal <img> element.
                draw_onload();
            } else {
                // Copy src data if it exists in model.
                if (this.model.has('src')) {
                    console.log('render has src');
                    if (this.model.get('src') != '') {
                        console.log('render has OK src');
                        this.update_src();
                    }
                }
            }

            // I noticed problems if this update() function call was left out, e.g. second views of
            // my model would not initially receive CSS style properties.
            this.update();
        },

        update_src: function () {
            console.log('update_src');
            console.log('update_src A width, height: ', this.image.width, this.image.height);
            // Python --> JavaScript
            // Copy new value from Backbone model, apply to this View.

            this.image.src = this.model.get('src');
            console.log('update_src B width, height: ', this.image.width, this.image.height);

            this.model.set('width', this.image.width);
            this.model.set('height', this.image.height);

            // this.draw() is called automatically and asynchronously via event handler installed
            // earlier in method this.render().
        },

        update_width: function () {
            // Python --> JavaScript
            // Copy new value from Backbone model, apply to this View.
            var value = this.model.get('width');
            this.canvas.width = value
            this.canvas.style.width = value + 'px'
        },

        update_height: function () {
            // Python --> JavaScript
            // Copy new value from Backbone model, apply to this View.
            var value = this.model.get('height');
            this.canvas.height = value
            this.canvas.style.height = value + 'px'
        },

        draw: function () {
            // Draw image data from internal <img> to the <canvas>.
            console.log('draw');

            this.update_width();
            this.update_height();

            // Apply transform.
            // this.context.setTransform(1, 0, 0, 1.5, 0, 0);

            // Draw image to screen.
            this.context.drawImage(this.image, 0, 0);

            // Must call this.touch() after any modifications to Backbone Model data.
            // this.touch();
        },

        update_transformation: function () {
            // Model's `transformation`: Python --> JavaScript
            console.log('update_transformation');

            // Apply new transformation.
            // http://www.whatwg.org/specs/web-apps/current-work/multipage/the-canvas-element.html#transformations
            // https://developer.mozilla.org/en-US/docs/Web/Guide/HTML/Canvas_tutorial/Transformations
            var M = this.model.get('transformation');

            // M = [m11, m12, m21, m22, m13, m23]
            var m11, m12, m21, m22, m13, m23;
            m11 = M[0]
            m12 = M[1]
            m21 = M[2]
            m22 = M[3]
            m13 = M[4]
            m23 = M[5]

            console.log(m11, m12, m21, m22, m13, m23);
            console.log(this.context);

            this.context.setTransform(m11, m12, m21, m22, m13, m23);
            this.draw(this.image);

            // Must call this.touch() after any modifications to Backbone Model data.
            this.touch();
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
