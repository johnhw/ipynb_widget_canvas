#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup

# Nice summary for uploading to PyPi
# http://peterdowns.com/posts/first-time-with-pypi.html

version = '0.3.5'
url = 'https://github.com/Who8MyLunch/ipynb_canvas_widget'

download_url = '{}/tarball/{}'.format(url, version)

setup(name='widget_canvas',
      description='A canvas image widget for the IPython Notebook',
      version=version,

      author='Pierre V. Villeneuve',
      author_email='pierre.villeneuve@gmail.com',
      license='MIT',
      url=url,
      download_url=download_url,

      keywords=['widget', 'jupyter', 'notebook', 'canvas', 'html5'],

      packages=['widget_canvas'],
      install_requires=['pillow', 'jupyter', 'numpy', 'requests'],
      package_data={'': ['*.txt', '*.js']},
      )
