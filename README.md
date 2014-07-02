
# A Canvas Widget for IPython Notebook

## Motivation

The HTML5 Canvas Element is a powerful tool for displaying resolution-dependent bitmap data.  It's great for efficiently rendering 2D graphics, images, artwork, or game components.  My current interest in the Canvas Element is to use it as the foundation for an interactive image viewer within the IPython [Notebook](http://ipython.org/notebook.html) widget [framework](http://nbviewer.ipython.org/github/ipython/ipython/blob/2.x/examples/Interactive%20Widgets/Index.ipynb).

I knew early on that I would need to learn a about JavaScript to make this project work. JavaScript is a really curious programming language, where the basic language itself is a wilderness of bizarre constructs.  Navigating through that is risky without a solid, practical reference [book](https://play.google.com/store/books/details/Douglas_Crockford_JavaScript_The_Good_Parts?id=PXa2bby0oQ0C). So many great external libraries and design patterns have developed over the years such that most people today seem to enjoy working with the language.  I was still surprised, however, at how much I had to learn about the [RequireJS](http://requirejs.org/) and [BackboneJS](http://backbonejs.org/) libraries before I could make significant progress on the technical parts.  I also found it very satisfying when the [Module Pattern](http://javascriptplayground.com/blog/2012/04/javascript-module-pattern/) started making sense to me.

## Design Thoughts

- My immediate plans for the Canvas Widget are to implement the functionality required by my
  other quantitative image viewer project.  This includes:

  - Display an image via URL
  - Display an image from a Numpy array: gray scale, RGB, or RGBA
  - Support image zooming and panning via mouse
  - Accept user-defined callback functions to be called as response to mouse motion/click events
  - Support for user-defined signal- and image-processing functions on Python back-end


- I want the basic framework to be generic such that adding support for other Canvas Element
  features in the future will be easy and fun.  Such features might include drawing geometric
  shapes, basic animation, and maybe even WebGL???  Contributions from other people would be
  welcome!

- Follow programming techniques (Python and JavaScript) observed in IPython's built-in Notebook
  widgets.  I would like for this widget to be as easy (or as hard??) to use as the built-in
  widgets.

- Image data accessed as a Python class property in a form compatible with a Numpy array.

- Image data synchronized between front- and back-end as Base64-encoded PNG-compressed data.

- The fundamental data structure synchronized between the back- and front-end is a `src` string
  containing a valid URL one could use to display an image using the HTML Image Element `<img>`.
  This is similar to how the IPython built-in Image Widget manages its data.  Note that it is quite
  straightforward to embed compressed image data as a large string within a URL description.

- The direct and programmatic display of image data will be facilitated by a second derived class
  that fully automates the process of creating URLs with embedded data.  The user will be exposed
  at the back-end to a class property containing a Numpy array of image data.


## Example Usage

TODO: link to my example notebook gist with nbviewer


## Reference Information

This is a list of the various web sites I found most helpful while learning new concepts
and solving my implementation problems.

- Comprehensive Canvas reference at [whatwg.org](http://whatwg.org) specifically for
  developers: [The Canvas Element](http://developers.whatwg.org/the-canvas-element.html).

- JavaScript [Design Patterns](http://addyosmani.com/resources/essentialjsdesignpatterns/book/)
  book by Addy Osmani.

- Fundamental BackboneJS information:
  [View](http://backbonejs.org/#View), [Model](http://backbonejs.org/#Model), and
  [Events](http://backbonejs.org/#Events)

- Life-saving nuggets of BackboneJS information:
  - StackOverflow discussion [rendering/appending views](http://stackoverflow.com/questions/9271507/how-to-render-and-append-sub-views-in-backbone-js)
  - list of [built-in events](http://backbonejs.org/#Events-catalog)
  - example handling [mouse click events](http://danielarandaochoa.com/backboneexamples/blog/2012/02/28/handling-the-click-event-with-backbone/)
  - Many more [great examples](http://backbonejs.org/#examples)


## Lessons Learned

- In my application I don't have a clean correspondence between a Python back-end variable and a
  simple HTML5/JavaScript front-end widget.  Instead I have an image and related cropping/scaling
  and offset parameters. I don't want to perform extra work and update all widget parameters when a
  single model parameter is changed. Some update are low overhead, e.g. redraw the image, while
  others require a lot of work, e.g. receive new PNG-compressed image data and copy it into the
  internal `Image` element.

  The best solution I've found to date is to forgo performing any work in my Backbone View's
  `this.update()` method, and instead use separate event handlers for each major part of my model.
  These may be defined in `this.initialize()` or in `this.render()`, but to me it seems more
  elegant to define them up in `this.initialize()`.  It might look like this:

  ```javascript
  this.model.on('change:_src', this.update_src, this);
  this.model.on('change:_width', this.update_width, this);
  this.model.on('change:_height', this.update_height, this);
  ```

- The method `this.update()` method in my extended JavaScript widget class is called automatically
  for all 'change' events triggered by IPython's Traitlet synchronization process.  This is
  implemented by the parent class `DOMWidgetView` via the method `initialize()` with a statement
  similar to the following:

  ```javascript
  this.model.on('change', this.update, this);
  ```

- In JavaScript I found that I need to call `this.update()` at the end of `this.render()`, even if
  my own `this.update()` doesn't do anything (or maybe doesn't even exist!).  I noticed odd
  problems when `this.update()` was left out, e.g. a second view of my model would not reflect
  any prior CSS style properties applied to earlier view instances.

- Here is how to check if a given variable exists within the application's Backbone Model:

  ```javascript
  if (this.model.has('_src')) {
      this.update_src();
  }
  ```

  I got this from the source: [backbonejs.org/#Model-has](http://backbonejs.org/#Model-has).  This
  was quite useful to decide if I needed to call (or not call) any expensive functions as part of
  `this.render()` or `this.update()`.  In particular, I needed this in order to properly display a
  secondary view of my widget after having already displayed the first view.  The Model was fully
  configured at this point and ready for rendering.  With the initial view, I instead rely on a
  data-changed event handler to call the `draw()` method.

- The Canvas Element height and width properties were initially quite confusing for me.  That's
  because its a two-part problem! 1) the Canvas has an inherent width and height measured in data
  pixels; 2) the Canvas as displayed to the screen is controlled by the element's CSS width and
  height. The StackOverflow discussion
  [canvas-width-and-height-in-html5](http://stackoverflow.com/questions/4938346/canvas-width-and-height-in-html5)
  was extremely helpful.

- More on Canvas width and height: I found I could not rely on the style width and height to always
  default to the Canvas' inherent width and height properties after several changes.  I'm not sure
  why. Maybe I did something wrong?  Maybe something to do with the IPython Notebook environment?
  My solution was to explicitly set the Canvas style width and height whenever I needed to modify
  the Canvas' inherent width and height.

- JavaScript mouse events are interesting:

  Event       | Description
  ---         | ---
  mousedown   | mouse button is pressed on an element.
  mouseup     | mouse button is released over an element.
  mousemove   | mouse is moved over an element.
  mouseenter  | mouse is moved onto the element that has the listener attached.
  mouseleave  | mouse is moved off the element that has the listener attached.
  mouseover   | mouse is moved onto the element that has the listener attached or onto one of its children.
  mouseout    | mouse is moved off the element that has the listener attached or off one of its children.

- Understanding `Canvas Element` mouse
  [coordinates](http://www.html5canvastutorials.com/advanced/html5-canvas-mouse-coordinates/)
  and
  [events](http://stackoverflow.com/questions/10001283/html5-canvas-how-to-handle-mousedown-mouseup-mouseclick#)
  in the context of BackbonJS
  [event handling](http://danielarandaochoa.com/backboneexamples/blog/2012/02/28/handling-the-click-event-with-backbone/)

- The built-in IPython `DOMWidget` has methods for handling CSS styles.  Use those methods instead
  of building my own handlers for particular style properties, e.g. border thickness and color.

- The notebook about IPython's
  [Traitlet Events](http://nbviewer.ipython.org/github/ipython/ipython/blob/2.x/examples/Interactive%20Widgets/Widget%20Events.ipynb#Traitlet-Events)
  gives a lot of insight into the relationship between front-end widgets and back-end data
  structures.  IPython's built-in widgets generally connect a simple data type (an integer or
  float, a list of values, etc.) to a simple widget (slider, checkbox, dropdown list).  This
  explains why most built-in widgets focus on synchronizing a `value` property between Python and
  JavaScript.  The `ButtonWidget` is one built-in is a slightly more complicated example. It
  doesn't manage any data, instead it generates `click` events, and it's framework is adapted to
  manage custom events.  I think the current version of `ButtonWidget` is more complicated than
  necessary.  Should not have to send custom messages, but instead rely on synchronized Traitlets.
  See this project's mouse event handling for an alternative and simpler example.
