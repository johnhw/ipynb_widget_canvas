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

setup(name='widget_canvas',
      description='A canvas image widget for the IPython Notebook',
      version='0.2.0',

      author='Pierre V. Villeneuve',
      author_email='pierre.villeneuve@gmail.com',
      license='MIT',
      url='https://github.com/Who8MyLunch/ipynb_canvas_widget',

      install_requires=['ipython', 'numpy', 'imageio', 'requests'],
      packages=['widget_canvas'],
      cmdclass=cmdclass('widget_canvas'),
      include_package_data=True,
      )
