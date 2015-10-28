#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup

# jupyter-pip
# Allows IPython notebook extension writers to make their extension pip installable!
# https://github.com/jdfreder/jupyter-pip
try:
    from jupyterpip import cmdclass
except:
    import pip
    import importlib
    pip.main(['install', 'jupyter-pip'])
    cmdclass = importlib.import_module('jupyterpip').cmdclass

#################################################

version = '0.3.3'
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

      keywords=['widget', 'ipython', 'notebook', 'canvas', 'html5'],

      packages=['widget_canvas'],
      install_requires=['pillow', 'ipython', 'numpy', 'requests'],
      cmdclass=cmdclass('widget_canvas'),
      include_package_data=True,
      )

# Nice summary for uploading to PyPi
# http://peterdowns.com/posts/first-time-with-pypi.html
