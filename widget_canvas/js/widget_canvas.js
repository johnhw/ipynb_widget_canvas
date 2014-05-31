//============================================================================
// CanvasWidget
//============================================================================

require(["widgets/js/widget"], function (WidgetManager) {

    console.log('require widget_canvas.js');

    // Define the widget's View.
    var CanvasView = IPython.DOMWidgetView.extend({
        initialize: function (options) {
            console.log('initialize');

            // Backbone model --> JavaScript
            this.model.on('change:_src', this.update_src, this);
            this.model.on('change:_height', this.update_height, this);
            this.model.on('change:_width', this.update_width, this);

            CanvasView.__super__.initialize.apply(this, arguments);
        },

        render: function () {
            // Render a widget's view instance to the DOM.
            console.log('render');

            // This project's view is quite simple: just a single <canvas> element.
            this.setElement('<canvas />');

            // Gather some handy references for the canvas and its context.
            this.canvas = this.el
            this.context = this.canvas.getContext('2d');

            // Internal image element serving to render new image src data.  This object will later
            // be used as source data argument to the canvas' own `drawImage()` method.
            this.image = new Image();

            // Draw content to the canvas if image data currently exists in the model.
            if (this.model.has('_src')) {
                this.update_width(false);
                this.update_height(false);
                this.update_src();
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

        update_width: function (call_draw) {
            // Python --> JavaScript
            console.log('update_width');

            // Default parameter value.
            call_draw = typeof call_draw !== 'undefined' ? call_draw : true

            this.canvas.width = this.model.get('_width');
            this.canvas.style.width = this.model.get('_width') + 'px'

            // Changing width or height automatically clears the display so we need to redraw it.
            if (call_draw) this.draw_image();
        },

        update_height: function (call_draw) {
            // Python --> JavaScript
            console.log('update_height');

            call_draw = typeof call_draw !== 'undefined' ? call_draw : true

            this.canvas.height = this.model.get('_height');
            this.canvas.style.height = this.model.get('_height') + 'px'

            // Changing width or height atomatically clears the display so we need to redraw it.
            if (call_draw) this.draw_image();
        },

        update_src: function () {
            // Python --> JavaScript
            console.log('update_src');

            // Copy image src from Backbone model to internal <img> element.
            this.image.src = this.model.get('_src');

            // Redraw display.
            this.draw_image();
        },

        draw_image: function () {
            // Draw image data from internal <img> to the <canvas>.
            console.log('draw_image');

            if (this.model.has('_src')) {
                if (this.model.get('_src') != '') {
                    // Draw image to screen and apply transform.
                    this.context.drawImage(this.image, 0, 0);
                }
            }
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

        // Mouse events.
        // https://developer.mozilla.org/en-US/docs/Web/Reference/Events/mousemove
        _build_mouse_event: function (ev) {
            // http://stackoverflow.com/questions/17130395/canvas-html5-real-mouse-position
            // https://developer.mozilla.org/en-US/docs/Web/API/Element.getBoundingClientRect
            var rect = this.canvas.getBoundingClientRect();
            var x = ev.clientX - rect.left
            var y = ev.clientY - rect.top

            var info = {
                canvasX: x,
                canvasY: y
            }

            // Copy select system mouse event attributes over to this application's mouse event
            // structure.
            var attributes = ['type', 'timeStamp', 'button',
                'ctrlKey', 'altKey', 'shiftKey', 'metaKey',
                'clientX', 'clientY'
            ]

            var key, ix
            for (ix in attributes) {
                key = attributes[ix]
                info[key] = ev[key]
            }

            return info
        },

        handle_mouse: function (ev) {
            // Event handler responding to mouse motion and button clicks.
            var info = this._build_mouse_event(ev)
            this.model.set('_mouse', info);

            // Must call this.touch() after any modifications to model data.
            this.touch();
        },

    });

    // Register CanvasView with widget manager.
    console.log('register');
    WidgetManager.register_widget_view('CanvasView', CanvasView);
});
