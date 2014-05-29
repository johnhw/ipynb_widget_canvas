
# Canvas Widget for IPython Notebook

## Motivation

The HTML5 Canvas Element is a nice tool for displaying resolution-dependent bitmap data.  It's
great for efficiently rendering 2D graphics, images, artwork, or game components.  My current
interest in the canvas element is to use it as the foundation for an interactive image viewer
within the IPython [Notebook](http://ipython.org/notebook.html) widget
[framework](http://nbviewer.ipython.org/github/ipython/ipython/blob/2.x/examples/Interactive%20Widgets/Index.ipynb).

todo: thoughts about ipython notebook, widgets, combined data processing, documentation, interactive exploration

I knew early on that I would need to learn a about JavaScript to make this project work. JavaScript
is a really curious programming language, where the basic language itself is a wilderness of of
bizarre constructs.  Navigating through that is risky without a solid, practical reference
[book](https://play.google.com/store/books/details/Douglas_Crockford_JavaScript_The_Good_
Parts?id=PXa2bby0oQ0C). So many great external libraries and design patterns have developed over
the years such that most people today seem to enjoy working with the language.  I was still
surprised, however, at how much I had to learn about the [RequireJS](http://requirejs.org/) and
[BackboneJS](http://backbonejs.org/) libraries before I could make significant progress on the
technical parts.  I also found it very satisfying when the [Module
Pattern](http://javascriptplayground.com/blog/2012/04/javascript-module-pattern/) started making
sense to me.


## Design Thoughts

- A basic canvas widget should simply expose basic canvas properties and methods from the
  JavaScript side over to the Python side.
- I have no immediate plans to implement any functionality other than what's needed for my image
  display and manipulation goals.
- I should also keep in mind that others might want to extend from my work to implement other kinds
  of canvas drawing functions.
- An important goal is support future objective for building a nice quantitative image viewing
  tool.  But that stuff could be done on top of a basic, general-purpose canvas widget.  Keep the
  widget simple and focus on managing function calls in JavaScript and event handling on either
  end.
- An image is stored and transfered between front- and backend as Base64-encoded png-compressed
  image src string.  From the user's point of view this is not so practical.  The user-facing
  Python interface will be nicer if it involves a Numpy array.  Internally I can process and
  convert to png compressed src string.  The src property is a traitlet and is thus synced
  automatically.  I can expose the Python image variable as a property.


## Example Usage

link to a notebook on nbviewer


## Reference Information

This section is a list of the various web sites I found most helpful while learning new concepts
and solving my implementation problems.

- Comprehensive canvas reference at [whatwg.org](http://whatwg.org) specifically for
developers: [The Canvas Element](http://developers.whatwg.org/the-canvas-element.html)
-
- Be sure to understand the meaning of Canvas element's inherent width & height versus the same element's CSS width & height.  The discussion on [StackOverflow](http://stackoverflow.com/questions/4938346/canvas-width-and-height-in-html5)

- JavaScript canvas mouse coordinate [awesome example](http://www.html5canvastutorials.com/advanced/html5-canvas-mouse-coordinates/)
- JavaScript canvas mouse click and motion handling: [example code](http://stackoverflow.com/questions/10001283/html5-canvas-how-to-handle-mousedown-mouseup-mouseclick#)


## Lessons Learned

- The method `this.update()` method in my derived JavaScript widget class is called automatically
  for all IPython Traitlet 'change' events.  This was configured via the parent class
  `DOMWidgetView` from the method `initialize()` with code similar to the following:

```javascript
  this.model.on('change', this.update, this);
```

In my application I don't have a simple correspondence between a Python variable and an
HTML/JavaScript widget parameter.  Instead I have an image, related cropping/offset paramters, and
overall width & height.  I don't wish to update all widget parameters when a new model parameter is
updated.  Some update are low overhead, e.g. redraw the image, while others require a lot of work,
e.g. receive new PNG-compressed image data and copy it into the internal `Image` element.

  The best solution I've found to date is to forgo performing any work in my class' `this.update()` method, and instead use separate event handlers for each major part of my model.  These may be defined in `this.initialize()` or in `this.render()`, but to me it seems more elegant to define them up in `this.initialize()`.  It might look like this
```javascript
    this.model.on('change:_src', this.update_src, this);
```
for establishing the event handler associated with the `_src` traitlet defined in the Python back end.

- **JS**: Need to call `this.update()` at the end of `this.render()`, even if my own `this.update()` doesn't do anything or maybe doesnt even exist.  I noticed odd problems if this update() function was left out, e.g. a second view of my model would not reflect any prior CSS style properties applied when only initial view existed.

- **JS**: Check whether or not a given variable exists within Backbone model: http://backbonejs.org/#Model-has
```javascript
    if (this.model.has('_src')) {
        this.update_src();
    }
```
  I found this quite useful to decide if I needed to call (or not call) any expensive functions as part of `this.render()` or `this.update()`.  In particular, I needed this in order to properly display a secondary view of my widget after having already displayed the first view.  The problem I had was that my image wold not display upon rendering the second view without this check in place.

- **JS**: Be sure to understand the meaning of Canvas element's inherent width & height versus the same element's CSS width & height.  The discussion on [StackOverflow](http://stackoverflow.com/questions/4938346/canvas-width-and-height-in-html5) proved to be very helpful.  In addition, I found I could not rely on the style width and height to always default to the canvas' width and height properties after several changes.  I'm not sure why.  Something to do with the IPython Notebook environment??

- JavaScript mouse events are interesting:

Mouse Event | Event Description
---         | ---
mousedown   | mouse button is pressed on an element.
mouseup     | mouse button is released over an element.
mousemove   | mouse is moved over an element.
mouseenter  | mouse is moved onto the element that has the listener attached.
mouseleave  | mouse is moved off the element that has the listener attached.
mouseover   | mouse is moved onto the element that has the listener attached or onto one of its children.
mouseout    | mouse is moved off the element that has the listener attached or off one of its children.

- The built-in IPython `DOMWidget` has methods for handling CSS styles.  Use those methods instead
  of building my own handlers for particular style properties, e.g. border thickness and color.

- **Traitlet Events**:  The discussion about [Specialized Events](http://nbviewer.ipython.org/github/ipython/ipython/blob/2.x/examples/Interactive%20Widgets/Widget%20Events.ipynb#Specialized-Events) gives a lot of insight into the relationship between frontend-widgets and backend data structures.  IPython's builtin widgets generally connect a simple data type (an integer or float, a list of values, etc.) to a simple widget (slider, checkbox, dropdown list).  This explains why most builtin widgets focus on synchronizing the `value` traitlet between the front and the back.  The `Button` widget is one builtin example of a slightly more complicated example.  It doesn't manage any data, instead it generates `click` events, and the framework is adapted to work with this widget's specific events.  I think the current version of ButtonWidget is more complicated than necessary.  Should not have to send custom messsages, instead rely on traitlets for synchronization.  Could also update the button to support PNG data for graphics.

  See also this notebook abot [Trait Events](http://nbviewer.ipython.org/github/ipython/ipython/blob/2.x/examples/Interactive%20Widgets/Widget%20Events.ipynb#Traitlet-Events).









- IPython Notebook [Specialized Events](http://nbviewer.ipython.org/github/ipython/ipython/blob/2.x/examples/Interactive%20Widgets/Widget%20Events.ipynb#Specialized-Events) gives a lot of insight into the relationship between frontend-widgets and backend data structures.


IPython's builtin widgets generally connect a simple data type (an integer or float, a list of
values, etc.) to a simple widget (slider, checkbox, dropdown list).  This explains why most builtin
widgets focus on synchronizing the `value` traitlet between the front and the back.  The `Button`
widget is one builtin example of a slightly more complicated example.  It doesn't manage any data,
instead it generates `click` events, and the framework is adapted to work with this widget's
specific events.  I think the current version of ButtonWidget is more complicated than necessary.
Should not have to send custom messsages, instead rely on traitlets for synchronization.  Could
also update the button to support PNG data for graphics.

  See also this notebook about [Trait Events](http://nbviewer.ipython.org/github/ipython/ipython/blob/2.x/examples/Interactive%20Widgets/Widget%20Events.ipynb#Traitlet-Events).


## JavaScript Frontend Actions

- Initialize HTML element(s)
- Connect Canvas events to Backbone events
    + Mouse click
    + Mouse move
    + Mouse wheel scroll
- Receive & display new image data
- Receive & apply image transform data

## Python Backend Actions

- Receive Canvas/Backbone events
- Generate & send new transform data
- Accept new image data from user
- Compress new image data & send to the Frontend


## Python Demo App

- Combine my CanvasImageWidget with built-in IPython button and slider widgets.
- Zoom and rotate an image.
- Animate through a sequence of images.


