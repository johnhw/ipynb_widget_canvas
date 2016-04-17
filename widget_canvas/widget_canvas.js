require(["widgets/js/widget", "widgets/js/manager"], function(widget, manager) {


    /////////////////////////////////////////////////
    // Helper functions

    function findAncestor(elem, cls) {
        // http://stackoverflow.com/questions/22119673/find-the-closest-ancestor-element-that-has-a-specific-class
        while ((elem = elem.parentElement) && !elem.classList.contains(cls));
        return elem;
    }

    /////////////////////////////////////////////////

    // define(function (require) {
    //     var widget = require('widgets/js/widget');

    var CanvasImageView = widget.DOMWidgetView.extend({
        render: function() {
            // Backbone Model --> JavaScript View
            // Render a widget's view instance to the DOM.

            // This project's view is quite simple: just a single <canvas> element.
            // if (this.model.get('canvas_id') == undefined) {
            //     this.model.set('canvas_id', guid());
            // }
            // console.log(this.model.get('_uuid'));
            this.setElement('<canvas />');

            this.canvas = this.el
            this.canvas.className = 'my_canvas ' + this.model.get('_uuid')

            // Dedicated event handler(s) for some special cases
            // http://backbonejs.org/#Events-on
            this.model.on('change:_encoded_url', this.update_encoded, this);
            this.model.on('change:_something', this.something, this);

            // Internal image object serving to render new image src data.  This object will
            // later be used as source data argument to the canvas' own `drawImage()` method.
            this.imageWork = new Image();
            var that = this
            this.imageWork.onload = function() {
                that.draw()
            }

            // Ideas for handling keyboard events in the future:
            // http://stackoverflow.com/questions/3729034/javascript-html5-capture-keycode-and-write-to-canvas

            // Mouse event throttle
            this._mouse_timestamp = 0
            this._mouse_time_threshold = 50 // milliseconds

            // Prevent mouse cursor from changing to text selection mode.
            // http://stackoverflow.com/a/11805438/282840
            // when-i-click-on-a-canvas-and-drag-my-mouse-the-cursor-changes-to-a-text-selecti
            this.canvas.onmousedown = function(event) {
                event.preventDefault();
            };

            // Prevent page from scrolling with mouse wheel events over canvas
            // http://stackoverflow.com/questions/10313142/
            //        javascript-capture-mouse-wheel-event-and-do-not-scroll-the-page
            this.canvas.onwheel = function(event) {
                event.preventDefault();
            };

            // Prevent context menu popup from right-click on canvas
            this.canvas.oncontextmenu = function(event) {
                event.preventDefault();
            };

            this.update();
            this.update_encoded();
        },

        update: function() {
            // Python --> JavaScript (generic)
            // Copy new value from Backbone model, apply to this View.
            // This method handles updates for almost everything except a select few traitlets that
            // have dedicated update functions.

            // Currently canvas width and height are slaved (on the Pythn side) to image's
            // inherent width and height.  Later this might be upgraded to support canvas' builtin
            // affine transform functions.

            // Awesome article about resizing canvas and/or displayed element
            // http://webglfundamentals.org/webgl/lessons/webgl-resizing-the-canvas.html

            // Update canvas width and height.
            // if (this.model.get('_width_canvas') !== undefined) {
            this.canvas.width = this.model.get('_width_canvas')
                // } else {
                // https://developer.mozilla.org/en-US/docs/Web/API/Element/removeAttribute
                // this.canvas.removeAttribute('_width_canvas');
                // }

            // if (this.model.get('_height_canvas') !== undefined) {
            this.canvas.height = this.model.get('_height_canvas')
                // } else {
                // https://developer.mozilla.org/en-US/docs/Web/API/Element/removeAttribute
                // this.canvas.removeAttribute('_height_canvas');
                // }

            // Update CSS display width and height
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

            // Image rendering quality
            // https://developer.mozilla.org/en/docs/Web/CSS/image-rendering
            // auto, crisp-edges, pixelated
            if (this.model.get('pixelated')) {
                this.canvas.style.imageRendering = 'pixelated'
            } else {
                this.canvas.style.imageRendering = 'auto'
            }

            // Draw it!
            this.draw()

            return CanvasImageView.__super__.update.apply(this);
        },

        update_encoded: function() {
            // Python --> JavaScript
            var value = this.model.get('_encoded_url');
            if (value != '') {

                // Load encoded image data into worker image object.
                // this.imageWork.src = 'data:image/' + this.model.get('_format') + ';base64,' + value
                this.imageWork.src = value

                // Event processing and image decoding continues inside imageWork's onload() event
                // handler, which in turn calls this.draw() defined further below.
            }
        },

        something: function() {
            // Testing ideas and debugging problems.

            console.log('something')

            // http://stackoverflow.com/questions/5694986/how-can-i-clone-an-image-in-javascript
            // http://stackoverflow.com/questions/8467121/can-i-copy-a-javascript-image-object
            // http://www.w3schools.com/jsref/met_node_clonenode.asp

            // Multiple options for getting image data
            // var imageFinal = this.imageWork.cloneNode()
            // var data_url = this.canvas.toDataURL()
            // var width = this.model.get('width')
            // var height = this.model.get('height')

            // var image_static = new Image();

            // Find pre-rendered static image place holder.
            var n = 'static_image_' + this.model.get('_uuid')
            var cell = findAncestor(this.canvas, 'cell')
            var image_static = cell.getElementsByClassName(n)[0]; // there should exist just a single output element
            image_static.src = this.canvas.toDataURL();
            image_static.style.display = 'block'

            // Find all rendered instances
            // var elems = document.getElementsByClassName(this.model.get('_uuid'));
            // console.log(elems)
            // for (var i = 0; i < elems.length; i++) {
            //     var elem_canvas = elems[i]
            //     console.log(elem_canvas)
            // }

            // // Build new element output_area.  Alll these details learned by browsing rendered
            // // notebook and copying observed styles.  Quite time consuming!  Blah!
            // var output_area = document.createElement('div')
            // output_area.className = 'output_area'

            // var prompt = document.createElement('div')
            // prompt.className = 'prompt'

            // var output_subarea = document.createElement('div')
            // output_subarea.className = 'output_subarea output_jpeg output_execute_result'
            // // output_png output_result
            // // output_html rendered_html


            // // Assemble output_area
            // output_area.appendChild(prompt)
            // output_area.appendChild(output_subarea)
            // output_subarea.appendChild(image_static)

            // // Now its time to place the above finished output_area in the right spot.

            // // Attach new output_area as first child of current cell's output element.
            // var cell = findAncestor(this.canvas, 'cell')
            // var output = cell.getElementsByClassName('output')[0]; // there should exist just a single output element

            // // New element `output_area` needs to be placed as first child of element `output` in
            // // order to replicate appearance of displayed widgets.  Potential problem is that there
            // // may or may not exist other sibling `output_area` elements.

            // // Pre-existing output_area elements?
            // var existing_output_areas = output.getElementsByClassName('output_area')
            // if (existing_output_areas.length > 0) {
            //     // Place in front of pre-existing output_area elements
            //     output.insertBefore(output_area, existing_output_areas[0]);
            // } else {
            //     // Add as only child
            //     output.appendChild(output_area);
            // }


            // Copy style to static image.
            // https://developer.mozilla.org/en-US/docs/Web/API/Window/getComputedStyle
            // var completeStyle = window.getComputedStyle(this.canvas, null).cssText
            // image_static.style.cssText = completeStyle


            // document.getElementById("placehere").appendChild(image);
            // need to add to current cell's output element:
            // - output area
            //     - output_subarea, output_jpeg (or output_png)



            // See IPython.display.Image for max-width confinement example

            // http://stackoverflow.com/questions/7802744/adding-an-img-element-to-a-div-with-javascript
            // this.appropriate_cell_area['text/html'] = '<img src="' + dataURL + '" width="' + width + '">';

            // IPython.keyboard_manager.enable()
            // $(fig.parent_element).html('<img src="' + dataURL + '" width="' + width + '">');
        },

        remove: function() {
            // Widget is about to be removed from the front end display.

            // This is a place where I could potentially add functionality to replace canvas with a
            // static image. See matplotlib's nbagg for ideas:
            // https://github.com/matplotlib/matplotlib/blob/master/lib/matplotlib/backends/web_backend/nbagg_mpl.js
            // http://stackoverflow.com/questions/7802744/adding-an-img-element-to-a-div-with-javascript
            // http://stackoverflow.com/questions/5694986/how-can-i-clone-an-image-in-javascript
            // http://www.w3schools.com/jsref/met_node_clonenode.asp
            // http://stackoverflow.com/questions/8467121/can-i-copy-a-javascript-image-object


            CanvasImageView.__super__.remove.apply(this, arguments);
        },

        clear: function() {
            // Clear the canvas while preserving current geometry state.
            // http://stackoverflow.com/a/6722031/282840
            var context = this.canvas.getContext('2d');

            context.save();

            context.setTransform(1, 0, 0, 1, 0, 0);
            context.clearRect(0, 0, this.canvas.width, this.canvas.height);

            context.restore();
        },

        draw: function() {
            // Draw image data from internal Image object to the Canvas element.
            // http://www.w3.org/TR/2014/CR-2dcontext-20140821/#drawing-images-to-the-canvas

            // Clear any prior image data.
            this.clear();

            // Update current transform information.
            // -= NOT YET IMPLEMENTED =-

            // Draw image to screen
            var context = this.canvas.getContext('2d');
            context.drawImage(this.imageWork, 0, 0);
        },

        /////////////////////////////////////////
        // JavaScript --> Python
        // Tell Backbone how to respond to JavaScript-generated events
        // Great reference: https://developer.mozilla.org/en-US/docs/Web/Reference/Events
        events: {
            mousemove: 'handle_mouse_move',
            mouseup: 'handle_mouse_generic',
            mousedown: 'handle_mouse_generic',
            wheel: 'handle_mouse_generic',
            click: 'handle_mouse_generic',
            // mouseenter: 'XXX',  // don't worry about these events for now
            // mouseleave: 'XXX',
            // mouseout:   'XXX',
            // mouseover:  'XXX',
        },

        build_mouse_event: function(jev) {
            // Build event data structure to be sent to Python backend

            // Mouse button events
            // https://developer.mozilla.org/en-US/docs/Web/API/MouseEvent/buttons
            //
            // Canvas-local XY coordinates:
            // http://stackoverflow.com/questions/17130395/canvas-html5-real-mouse-position
            // https://developer.mozilla.org/en-US/docs/Web/API/Element.getBoundingClientRect
            var rect = this.canvas.getBoundingClientRect();

            // Convert event types to more practical values for user's Python callback functions.
            var js_to_py = {
                'mousemove': 'move',
                'mouseup': 'up',
                'mousedown': 'down',
                'click': 'click',
                'wheel': 'wheel',
            }

            // Build the event
            var ev = {
                type: js_to_py[jev.originalEvent.type],
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

        check_mouse_throttle: function(jev) {
            // Return true if enough time has passed
            var delta = jev.originalEvent.timeStamp - this._mouse_timestamp
            if (delta >= this._mouse_time_threshold) {
                this._mouse_timestamp = jev.originalEvent.timeStamp
                return true
            } else {
                return false
            }
        },

        handle_mouse_generic: function(jev) {
            // Generic mouse event handler
            // https://developer.mozilla.org/en-US/docs/Web/Reference/Events
            if (this.model.get('_mouse_active')) {
                var ev = this.build_mouse_event(jev);
                this.model.set('_mouse_event', ev);
                this.touch(); // Must call after any modifications to Backbone Model data.
            }
        },

        handle_mouse_move: function(jev) {
            // Mouse motion event handler
            if (this.model.get('_mouse_active')) {
                if (this.check_mouse_throttle(jev)) {
                    // This event appears to generate a lot of CPU usage.  Throttling is my
                    // simple attempt to mitigate the issue.
                    var ev = this.build_mouse_event(jev);
                    this.model.set('_mouse_event', ev);
                    this.touch(); // Must call after any modifications to Backbone Model data.
                }
            }
        },
    });

    // Simple way to load JS stuff.
    manager.WidgetManager.register_widget_view('CanvasImageView', CanvasImageView);

    // // Official and complicated way to load/register JS stuff.
    // return {
    //     CanvasImageView: CanvasImageView,
    // };
});
