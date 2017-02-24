from __future__ import print_function
from functools import partial
from operator import add, sub, mul, div

"""Goals:

    * To be able to use the toolz library in my pipelines
    * Should work with Pandas, Numpy and Matplotlib
    * Deal with dict.update(...)
    * Deal with pd.DataFrame.sort(...)
    * Allow Lambdas to build up into complex expressions
    * Lambdas and Pipes should play nicely together
    * Allow using Pipes to build up pipelines
    * Allow working with iterators and streams
"""


class Lambda(object):

    def __init__(self):
        pass

    def __getattr__(self, attr):
        pass

    def __add__(self, other):
        return partial(add, other)

    def __sub__(self, other):
        return partial(sub, other)

    def __mul__(self, other):
        return partial(mul, other)

    def __div__(self, other):
        return partial(div, other)

_ = Lambda()


class Pipe(object):

    def __init__(self):
        pass

    def __call__(self, state):
        self.state = state
        return self

    def __rshift__(self, function):
        if callable(function):
            self.state = function(self.state)
            return self
        elif function is None:
            return self.state
        else:
            raise ValueError("{!r}: {!r}".format('function', function))

    def __lshift__(self, function):
        "Like >> but doesn't update the state"
        if callable(function):
            function(self.state)
            return self
        elif function is None:
            return self.state
        else:
            raise ValueError("{!r}: {!r}".format('function', function))


pipe = Pipe()
do = Pipe()


if __name__=='__main__':
    print(pipe(5) >> (lambda n: n*2) >> (lambda n: n+1) >> None)
    print(pipe(5) >> _*2 >> _+1 >> None)
    print(do(xrange(3)) >> list >> None)
    do(xrange(3)) \
        >> list \
        << print \
        >> (lambda l: map(_*2,l)) \
        << print \
        >> None
