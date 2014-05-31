
from setuptools import setup, find_packages

# Do it.
version = '0.0.1'

setup(name='ipynb_widget_canvas',
      packages=find_packages(),
      package_data={'': ['*.txt', '*.md', '*.py', '*.ipynb',  '*.']},

      # Metadata
      version=version,
      license='MIT',
      author='Pierre V. Villeneuve',
      author_email='pierre.villeneuve@gmail.com',
      description='A Canvas Widget for the IPython Notebook',
      url='https://github.com/Who8MyLunch/ipynb_canvas_widget')
