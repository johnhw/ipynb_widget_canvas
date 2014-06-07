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
            // this.model.on('change:_height', this.update_height, this);
            // this.model.on('change:_width', this.update_width, this);
            CanvasView.__super__.initialize.apply(this, arguments);
        },

        render: function () {
            // Render a widget's view instance to the DOM.
            // console.log('render');

            // This project's view is quite simple: just a single <canvas> element.
            this.setElement('<canvas />');

            // Gather some handy references for the canvas and its context.
            this.canvas = this.el
            this.context = this.canvas.getContext('2d');

            // Internal image element serving to render new image src data.  This object will later
            // be used as source data argument to the canvas' own `drawImage()` method.
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

        //         update: function() {
        //             // Python --> JavaScript
        //             console.log('update');
        //             //
        //             // This method is called automatically for all traitlet 'change' events.  This
        //             // was configured via the builtin widget.js from the method WidgetView.initialize()
        //             // and again in DOMWidgetView() with code similar to the following:
        //             //
        //             // this.model.on('change', this.update, this);
        //             //
        //             // I'm using separate event handlers for each major part of my model and not
        //             // relying upon this single all-encompassing event handler.
        //             //
        //             return CanvasView.__super__.update.apply(this);
        //             },
        // update_width: function (call_draw) {
        //     // Python --> JavaScript
        //     // console.log('update_width');
        //     // Default parameter value.
        //     call_draw = typeof call_draw !== 'undefined' ? call_draw : true
        //     var value = this.model.get('_width');
        //     if (value == 0) {
        //         value = this.image.width
        //     }
        //     this.canvas.width = value
        //     this.canvas.style.width = value + 'px'
        //     // Changing width or height automatically clears the display so we need to redraw it.
        //     if (call_draw) this.draw_image();
        // },
        // update_height: function (call_draw) {
        //     // Python --> JavaScript
        //     // console.log('update_height');
        //     call_draw = typeof call_draw !== 'undefined' ? call_draw : true
        //     var value = this.model.get('_height');
        //     if (value == 0) {
        //         value = this.image.height
        //     }
        //     this.canvas.height = value
        //     this.canvas.style.height = value + 'px'
        //     // Changing width or height atomatically clears the display so we need to redraw it.
        //     if (call_draw) this.draw_image();
        // },

        update_src: function () {
            // Python --> JavaScript
            // console.log('update_src');

            // call_draw = typeof call_draw !== 'undefined' ? call_draw : true

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

        /////////////////////////////////////////////
        // JavaScript --> Python
        // Tell Backbone how to respond to JavaScript-generated events.
        //
        // Great reference for JavaScript events:
        // https://developer.mozilla.org/en-US/docs/Web/Reference/Events
        events: { //'click': 'handle_click',
            'mousemove': 'handle_mouse',
            'mouseup': 'handle_mouse',
            'mousedown': 'handle_mouse',
            //                  'mouseenter': 'handle_mouse',  // don't worry about these other mouse
            //                  'mouseleave': 'handle_mouse',  // events for now.
            //                  'mouseout':   'handle_mouse',
            //                  'mouseover':  'handle_mouse',
        },

        // Extract information about a mouse event.
        // https://developer.mozilla.org/en-US/docs/Web/Reference/Events/mousemove
        _build_mouse_info: function (ev) {
            // http://stackoverflow.com/questions/17130395/canvas-html5-real-mouse-position
            // https://developer.mozilla.org/en-US/docs/Web/API/Element.getBoundingClientRect
            var rect = this.canvas.getBoundingClientRect();
            var x = ev.clientX - rect.left
            var y = ev.clientY - rect.top

            var info = {
                canvasX: x,
                canvasY: y,
            }

            // Copy select system mouse event attributes over to this application's mouse event
            // structure.
            var attributes = ['type', 'timeStamp', 'button',
                'ctrlKey', 'altKey', 'shiftKey', 'metaKey',
                'clientX', 'clientY',
            ]

            var key, ix
            for (ix in attributes) {
                key = attributes[ix]
                info[key] = ev[key]
            }

            return info
        },

        // Handle a mouse event.
        handle_mouse: function (ev) {
            // Event handler responding to mouse motion and button clicks.
            var info = this._build_mouse_info(ev)
            this.model.set('_mouse', info);

            // Must call this.touch() after any modifications to Backbone Model data.
            this.touch();
        },

    });

    // Register View with widget manager.
    // console.log('register');
    WidgetManager.register_widget_view('CanvasView', CanvasView);
});
