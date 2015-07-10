
from __future__ import print_function, unicode_literals, division, absolute_import

"""
Derived from http://stackoverflow.com/questions/5849800/tic-toc-functions-analog-in-python
"""

import os
import time

class Timer(object):
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.time_start = None
        self.time_end = None

    def __enter__(self):
        self.time_start = time.time()

        return self

    def __exit__(self, type, value, traceback):
        self.time_end = time.time()

        if self.verbose:
            self.pretty_print()


    @property
    def time(self):
        if self.time_end is None or self.time_end is None:
            return None
        else:
            return self.time_end - self.time_start


    def pretty_print(self):
        print('Run time: {:.4f} sec.'.format(self.time))



if __name__ == '__main__':
    """
    Example.
    """

    def fn():
        # dummy function.
        t = 1.010101
        time.sleep(t)
        return t


    with Timer(verbose=True) as t:
        print('sdsdfsdsdfs')
        d = fn()

    print(t.time)

    print('sad')
