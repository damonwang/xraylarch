#!/usr/bin/env python

from __future__ import with_statement
import os
import sys
import unittest
from contextlib import contextmanager
import tempfile
import ast
import larch

#------------------------------------------------------------------------------

@contextmanager
def fake_call(original, replacement):
        '''context manager that swaps out a function when called with the
        given arguments. To be used for testing, not production.

        Args:
            original: function to replace
            replacement: function that answers some (possibly improper) subset
                of calls to original
        '''

        orig_mod = sys.modules[original.__module__]
        orig_name = original.__name__

        def dummy(*args, **kwargs):
            '''intercepts calls to original and substitutes replacement'''
            try: return replacement(*args, **kwargs)
            except KeyError: return original(*args, **kwargs)
    
        setattr(orig_mod, orig_name, dummy)
        yield
        setattr(orig_mod, orig_name, original)

#------------------------------------------------------------------------------

class TestCase(unittest.TestCase):
    def true(self, expr):
        '''assert that larch evaluates expr to True'''

        return self.assertTrue(self.li(expr))

    def false(self, expr):
        '''assert that larch evaluates expr to False'''

        return self.assertFalse(self.li(expr))

    def assertListEqual(self, A, B):
        '''A and B have the same items in the same order'''

        self.assert_(len(A) == len(B))
        for a, b in zip(A, B):
            self.assert_(a == b)

    def setUp(self):
        self.stdout = tempfile.NamedTemporaryFile(delete=False, prefix='larch')
        self.li = larch.Interpreter(writer=self.stdout)
        self.n = lambda : self.li.symtable.n

    def tearDown(self):
        if not self.stdout.closed:
            self.stdout.close()
        os.unlink(self.stdout.name)

    def eval(self, expr):
        '''evaluates expr in a way that the interpreter sometimes can't, for
        some reason. Appends a newline if necessary.
        '''

        if not expr.endswith('\n'):
            expr += '\n'

        return self.li.interp(ast.parse(expr))


#------------------------------------------------------------------------------

class TestFakeCall(TestCase):

    def test_fake_call(self):
        '''fake_call context manager'''
        PATH = os.getenv('PATH')
        HOME = os.getenv('HOME')
        with fake_call(os.getenv, dict(HOME='here').__getitem__):
            self.assert_(os.getenv('HOME') == 'here')
            self.assert_(os.getenv('HOME') != HOME)
            self.assert_(os.getenv('PATH') == PATH)

#------------------------------------------------------------------------------
