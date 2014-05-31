from __future__ import division, print_function, unicode_literals

import os

import simplejson as json

import dominate
import dominate.tags as dtags
import urlnorm

import numpy as np
import IPython
import IPython.html

#################################################
# Static variables

_path_module = os.path.abspath(os.path.dirname(__file__))
_path_js = os.path.join(_path_module, 'js')

_init_counter = 0


#################################################
# Helper functions

def _read_local_js(fname):
    """
    Read a JavaScript file from application's local JS folder.  Return as a string.
    """
    b, e = os.path.splitext(os.path.basename(fname))
    f = os.path.join(_path_js, b + '.js')

    if not os.path.isfile(f):
        raise IOError('File not found: {}'.format(f))

    with open(f) as fo:
        text = fo.read()

    return text


#################################################
# Main stuff

class ImageViewer(object):
    """
    An HTML image viewer for the IPython Notebook.
    """
    def __init__(self):
        """
        Create a new image viewer instance.
        """

        # Used to keep track of how many times this class was instanciated from this module.
        global _init_counter

        _init_counter += 1
        self.id_app = 'nb_app_{:d}'.format(_init_counter)
        self.id_canvas = self.id_app + '_canvas'

        self.initialize_js()

    def __repr__(self):
        """
        Summary description.
        """
        lines = ['Notebook Image Viewer',
                 # 'URL: {:s}'.format(self._url),
                 # 'width:  {:d}'.format(self.width),
                 # 'height: {:d}'.format(self.height),
                 '']

        return '\n'.join(lines)

    def _repr_html_(self):
        """
        Generate the HTML representation of this object for display with IPython's Rich Display
        system.
        """
        return self.generate_html()

    def display(self):
        """
        Render video player in the browser to Notebook's current cell.
        This uses IPython builtin rich display system.
        """
        IPython.display.display(self)

    #############################################

    def initialize_js(self):
        """
        Setup application objects in browser's global window namespace.  This does not need to be
        called for every video display.  At the most it should be called once per class instance.
        At the least it could be improved to be called once per browser session.
        """
        init_js = _read_local_js('init.js')
        IPython.display.display_javascript(init_js, raw=True)

    def nb_video_js(self):
        """
        Configure and run my JavaScript video player module.
        """
        info = {'url': self.url,
                'id_video': self.id_video,
                'width': self.width,
                'height': self.height}

        template = """
        var config = {:s}
        var player = window.nbv.new_player(config);
        """

        script = template.format(json.dumps(info, ensure_ascii=False))

        # Replace double quotes with single quotes, otherwise this combination of json.dumps() and
        # dominate.render() causes syntax errors in the browser.
        script = script.replace('"', "'")

        return script

    def generate_html(self):
        """
        Construct HTML document parts.
        """

        # Paramters.
        width_bkg = self.width
        height_bkg = self.height + 39

        title = 'Notebook Video Player'
        doc = dominate.document(title)

        with doc:

            link = dtags.link()
            link['href'] = 'nb_video/js/video-js/video-js.css'
            link['rel'] = 'stylesheet'
            link['type'] = 'text/css'

            container = dtags.div(id=self.id_app)
            with container:
                template = 'width:{:d}px;height:{:d}px;background-color:#5A5A5A;'
                style = template.format(width_bkg, height_bkg)

                bkg = dtags.div(style=style)
                with bkg:
                    video_class = 'video-js vjs-default-skin'

                    vid = dtags.video(id=self.id_video, width=self.width, height=self.height,
                                      cls=video_class, preload='auto')

                    with vid:
                        src = dtags.source()
                        src['src'] = self.url
                        src['type'] = 'video/mp4'

            # Javascript content with config details for this video.
            dtags.script(self.nb_video_js())

        # Done.
        return doc.render()
