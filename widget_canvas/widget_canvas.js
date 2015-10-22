define(function (require) {
    var widget = require('widgets/js/widget');

    var CanvasImageView = widget.DOMWidgetView.extend({
        render: function () {
            // Backbone Model --> JavaScript View
            // Render a widget's view instance to the DOM.

            // This project's view is quite simple: just a single <canvas> element.
            // http://stackoverflow.com/questions/3729034/javascript-html5-capture-keycode-and-write-to-canvas
            this.setElement('<canvas />');

            // Gather some handy references for the canvas and its context.
            this.canvas = this.el
            this.context = this.canvas.getContext('2d');

            // Dedicated event handler(s) for special cases, e.g. changes to encoded image data.
            // http://backbonejs.org/#Events-on
            this.model.on('change:_encoded', this.update_encoded, this);

            // Internal image object serving to render new image src data.  This object will
            // later be used as source data argument to the canvas' own `drawImage()` method.
            this.imageWork = new Image();
            var that = this
            this.imageWork.onload = function () {
                that.draw()
            }

            // Mouse event throttle.
            this._mouse_timestamp = 0
            this._mouse_time_threshold = 50 // milliseconds

            // Prevent mouse cursor from changing to text selection mode.
            // http://stackoverflow.com/a/11805438/282840
            // when-i-click-on-a-canvas-and-drag-my-mouse-the-cursor-changes-to-a-text-selecti
            this.canvas.onmousedown = function (event) {
                event.preventDefault();
            };

            // Prevent page from scrolling with mouse wheel events over canvas.
            this.canvas.onwheel = function (event) {
                event.preventDefault();
            };

            // Prevent right-click context menu.
            this.canvas.oncontextmenu = function (event) {
                event.preventDefault();
            };

            // Image rendering option
            // https://developer.mozilla.org/en/docs/Web/CSS/image-rendering
            // auto, crisp-edges, pixelated
            this.canvas.style.imageRendering = 'pixelated'
            // mozilla browsers might instead need to se '-moz-crisp-edges'??

            this.update();
            this.update_encoded();
        },

        update: function () {
            // Python --> JavaScript (generic)
            // Copy new value from Backbone model, apply to this View.
            // This method handles updates for almost everything except a select few that
            // dedicated update functions.

            // Currently canvas width and height are slaved to CSS/DOM width and height.
            // Later this might be upgraded to support canvas' builtin affine transform support.

            // Awesome article about resizing canvas and/or displayed element.
            // http://webglfundamentals.org/webgl/lessons/webgl-resizing-the-canvas.html

            // Update canvas width and height.
            if (this.model.get('width_canvas') !== undefined) {
                this.canvas.width = this.model.get('width_canvas')
            } else {
                // https://developer.mozilla.org/en-US/docs/Web/API/Element/removeAttribute
                this.canvas.removeAttribute('width');
            }

            if (this.model.get('height_canvas') !== undefined) {
                this.canvas.height = this.model.get('height_canvas')
            } else {
                // https://developer.mozilla.org/en-US/docs/Web/API/Element/removeAttribute
                this.canvas.removeAttribute('height');
            }

            // Update CSS display width and height.
            if (this.model.get('width') !== undefined) {
                this.canvas.style.width = this.model.get('width') + 'px'
            } else {
                // https://developer.mozilla.org/en-US/docs/Web/API/Element/removeAttribute
                this.canvas.style.removeAttribute('width');
            }

            if (this.model.get('height') !== undefined) {
                this.canvas.style.height = this.model.get('height') + 'px'
            } else {
                // https://developer.mozilla.org/en-US/docs/Web/API/Element/removeAttribute
                this.canvas.style.removeAttribute('height');
            }

            // Draw it!
            this.draw()

            return CanvasImageView.__super__.update.apply(this);
        },

        update_encoded: function () {
            // Python --> JavaScript
            var value = this.model.get('_encoded');
            if (value != '') {

                // Load encoded image data into worker image object.
                this.imageWork.src = 'data:image/' + this.model.get('_format') + ';base64,' + value

                // Event processing and image decoding continues inside imageWork's onload() event
                // handler, which in turn calls this.draw().
            }
        },

        clear: function () {
            // Clear the canvas while preserving current geometry state.
            // http://stackoverflow.com/a/6722031/282840
            this.context.save();

            this.context.setTransform(1, 0, 0, 1, 0, 0);
            this.context.clearRect(0, 0, this.canvas.width, this.canvas.height);

            this.context.restore();
        },

        draw: function () {
            // Draw image data from internal Image object to the Canvas element.
            // http://www.w3.org/TR/2014/CR-2dcontext-20140821/#drawing-images-to-the-canvas

            // Clear any prior image data
            this.clear();

            // Draw image to screen
            this.context.drawImage(this.imageWork, 0, 0);
        },

        /////////////////////////////////////////
        // JavaScript --> Python
        // Tell Backbone how to respond to JavaScript-generated events.
        // Great reference: https://developer.mozilla.org/en-US/docs/Web/Reference/Events
        events: {
            mousemove: 'handle_mouse_move',
            mouseup: 'handle_mouse_generic',
            mousedown: 'handle_mouse_generic',
            wheel: 'handle_mouse_generic',
            click: 'handle_mouse_generic',
            // mouseenter: 'XXX',  // don't worry about these events for now.
            // mouseleave: 'XXX',
            // mouseout:   'XXX',
            // mouseover:  'XXX',
        },

        _build_mouse_event: function (jev) {
            // Build event data structure to be passed along to Python backend.

            // Mouse button events
            // https://developer.mozilla.org/en-US/docs/Web/API/MouseEvent/buttons
            //
            // Canvas-local XY coordinates:
            // http://stackoverflow.com/questions/17130395/canvas-html5-real-mouse-position
            // https://developer.mozilla.org/en-US/docs/Web/API/Element.getBoundingClientRect

            var rect = this.canvas.getBoundingClientRect();

            var ev = {
                type: jev.originalEvent.type,
                canvasX: parseInt(jev.originalEvent.clientX - rect.left),
                canvasY: parseInt(jev.originalEvent.clientY - rect.top),
                shiftKey: jev.originalEvent.shiftKey,
                altKey: jev.originalEvent.altKey,
                ctrlKey: jev.originalEvent.ctrlKey,
                timeStamp: jev.originalEvent.timeStamp,
                buttons: jev.originalEvent.buttons,
            }

            // Check for `wheel` event
            // https://developer.mozilla.org/en-US/docs/Web/Reference/Events/wheel
            if (jev.originalEvent.type == 'wheel') {
                ev.deltaMode = jev.originalEvent.deltaMode
                ev.deltaX = jev.originalEvent.deltaX
                ev.deltaY = jev.originalEvent.deltaY
                ev.deltaZ = jev.originalEvent.deltaZ
            }

            return ev
        },

        _check_mouse_throttle: function (jev) {
            // Return true if enough time has passe
            var delta = jev.originalEvent.timeStamp - this._mouse_timestamp
            if (delta >= this._mouse_time_threshold) {
                this._mouse_timestamp = jev.originalEvent.timeStamp
                return true
            } else {
                return false
            }
        },

        handle_mouse_generic: function (jev) {
            // Generic mouse event handler
            // https://developer.mozilla.org/en-US/docs/Web/Reference/Events
            var ev = this._build_mouse_event(jev);
            this.model.set('_mouse_event', ev);
            this.touch(); // Must call after any modifications to Backbone Model data.
        },

        handle_mouse_move: function (jev) {
            // Mouse motion event handler
            // This event appears to generate a lot of CPU usage.  Throttling is my attempt to
            // mitigate the issue.
            if (this._check_mouse_throttle(jev)) {
                var ev = this._build_mouse_event(jev);
                this.model.set('_mouse_event', ev);
                this.touch(); // Must call after any modifications to Backbone Model data.
            }
        },
    });

    // All done.
    return {
        CanvasImageView: CanvasImageView,
    };
});