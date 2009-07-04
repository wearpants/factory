#!/usr/bin/env python
# encoding: utf-8

if __name__ == "__main__":
    import doctest
    import functools
    import itertools

    extraglobs = {'functools': functools,
                  'itertools': itertools,
                  '__name__': None} # fix __main__ issues

    doctest.testfile("README", extraglobs=extraglobs)
    doctest.testfile("PEP")
