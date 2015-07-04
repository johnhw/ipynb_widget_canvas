// An elephant image URL
var url = 'http://upload.wikimedia.org/wikipedia/commons/thumb/3/37/African_Bush_Elephant.jpg/160px-African_Bush_Elephant.jpg'

// Get the canvas element plus corresponding drawing context
var canvas = document.getElementById('hello_example');
var context = canvas.getContext('2d');

// Create a hidden <img> element to manage incoming data.
var img = new Image();

// Add new-data event handler to the hidden <img> element.
img.onload = function () {
    // This function will be called when new image data has finished loading
    // into the <img> element.  This new data will be the source for drawing
    // onto the Canvas.

    // Set canvas geometry.
    canvas.width = img.width
    canvas.style.width = img.width + 'px'

    canvas.height = img.height
    canvas.style.height = img.height + 'px'

    // Draw new image data onto the Canvas.
    context.drawImage(img, 0, 0);
}

// Assign image URL.
img.src = url