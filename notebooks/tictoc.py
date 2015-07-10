
from __future__ import print_function, unicode_literals, division, absolute_import

"""
Derived from http://stackoverflow.com/questions/5849800/tic-toc-functions-analog-in-python
"""

import time


class Timer(object):
    def __init__(self, verbose=True):
        self.verbose = verbose
        self.time_start = None
        self.time_end = None

    def __enter__(self):
        self.time_start = time.time()

        return self

    def __exit__(self, type, value, traceback):
        self.time_end = time.time()

        if self.verbose:
            print(self.pretty())

    @property
    def time(self):
        if self.time_end is None or self.time_end is None:
            return None
        else:
            return self.time_end - self.time_start

    def pretty(self):
        template = 'Run time: {:.3f} {}'

        t = self.time

        if t > 0.5:
            text = template.format(t, 's')
        elif t*1.e3 > 0.5:
            text = template.format(t*1.e3, 'ms')
        elif t*1.e6 > 0.5:
            text = template.format(t*1.e6, 'us')
        else:
            text = template.format(t*1.e9, 'ns')

        return text

    def __repr__(self):
        return self.pretty()


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
        print(d)

    print(t.time)

    print('sad')
