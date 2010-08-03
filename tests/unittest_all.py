#!/usr/bin/env python

from __future__ import with_statement
import os
import sys
import unittest
import optparse
from contextlib import contextmanager
from larch.symboltable import GroupAlias
from unittest_larchEval import TestLarchEval
from unittest_SymbolTable import TestSymbolTable
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

class TestMockCall(unittest.TestCase):

    def test_1(self):
        PATH = os.getenv('PATH')
        HOME = os.getenv('HOME')
        with fake_call(os.getenv, dict(HOME='here').__getitem__):
            self.assert_(os.getenv('HOME') == 'here')
            self.assert_(os.getenv('HOME') != HOME)
            self.assert_(os.getenv('PATH') == PATH)

#------------------------------------------------------------------------------

class TestGroupAlias(unittest.TestCase):

    def test_create(self):
        '''construct a group from an object instance'''

        # get a useful backtrace
        # must restore recursion limit or later tests will be VERY odd
        rec_lim = sys.getrecursionlimit()
        sys.setrecursionlimit(35)
        ga = GroupAlias({})
        sys.setrecursionlimit(rec_lim)

#------------------------------------------------------------------------------

class TestLarchImport(unittest.TestCase):

    def true(self, expr):
        '''assert that larch evaluates expr to True'''

        return self.assertTrue(self.li(expr))

    def false(self, expr):
        '''assert that larch evaluates expr to False'''

        return self.assertFalse(self.li(expr))

    def setUp(self):
        '''creates a larch interpreter'''

        self.li = larch.interpreter.Interpreter()

    def test_import(self):
        '''import entire python module'''

        self.li("import unittest")

        self.assert_(hasattr(self.li.symtable, 'unittest'))
        self.assert_(hasattr(self.li.symtable.unittest, 'TestCase'))

    def test_import_as(self):
        '''import entire python module as other name'''

        self.li("import unittest as test")

        self.assert_(hasattr(self.li.symtable, 'test'))
        self.assert_(hasattr(self.li.symtable.test, 'TestCase'))

    def test_from_import(self):
        '''import python submodule'''

        self.li("from unittest import TestCase")

        self.assert_(hasattr(self.li.symtable, 'TestCase'))
        self.assert_(hasattr(self.li.symtable.TestCase, 'assert_'))

    def test_from_import_as(self):
        '''import python submodule as other name'''

        self.li("from unittest import TestCase as tc")

        self.assert_(hasattr(self.li.symtable, 'tc'))
        self.assert_(hasattr(self.li.symtable.tc, 'assert_'))

    def test_larch_import(self):
        '''import entire larch module'''

        self.li("import random")

        self.assert_(hasattr(self.li.symtable, 'random'))
        print(dir(self.li.symtable.random))
        self.assert_(hasattr(self.li.symtable.random, 'weibull'))
        # make sure we didn't take the Python random module
        self.assert_(not hasattr(self.li.symtable.random, 'gauss'))

    def test_larch_from_import(self):
        '''import larch submodule'''

        self.li('from random import weibull')

        self.assert_(hasattr(self.li.symtable, 'weibull'))
        self.assert_(hasattr(self.li.symtable.weibull, '__call__'))

    def test_larch_from_import_as(self):
        '''import larch submodule as other name'''

        self.li('from random import weibull as wb')

        self.assert_(hasattr(self.li.symtable, 'wb'))
        self.assert_(hasattr(self.li.symtable.wb, '__call__'))

#------------------------------------------------------------------------------

class TestLarchSource(unittest.TestCase):
    '''interpreter can source larch code from strings, files, etc.'''

    def true(self, expr):
        '''assert that larch evaluates expr to True'''

        return self.assertTrue(self.li(expr))

    def false(self, expr):
        '''assert that larch evaluates expr to False'''

        return self.assertFalse(self.li(expr))

    def setUp(self):
        '''creates a larch interpreter'''

        self.li = larch.interpreter.Interpreter()

    def test_push_expr(self):
        '''push expression'''

        self.assert_(self.li.push("1"))

    def test_push_statement(self):
        '''push a statement'''

        self.assert_(self.li.push("a = 1"))

    def test_push_incomplete(self):
        '''push an incomplete construct'''

        self.assert_(not self.li.push("a = "))
        self.assert_(self.li.push("1"))
        self.assert_(self.li.symtable.a == 1)

    def test_push_SyntaxError(self):
        '''push a syntax error'''

        self.assertRaises(SyntaxError, self.li.push, "1 = a")

    def test_push_buf_local(self):
        '''push buffer is local to larch interpreter instance'''

        li2 = larch.interpreter.Interpreter()
        self.li.push("a = ")

        self.assert_(not hasattr(li2, 'push_buf'))

    def test_eval_file(self):
        '''eval a larch file'''

        # FIXME can't handle non-Python indentation yet
        larchcode = '''
a = 0
for i in arange(10):
    a += i
endfor'''

        fname="testingtmp"
        with open(fname, "w") as outf:
            print >> outf, larchcode

        self.assert_(self.li.eval_file(fname))
        self.assert_(self.li.symtable.a == 45)

        os.unlink(fname)

#------------------------------------------------------------------------------

def get_args():
    op = optparse.OptionParser()
    op.add_option('-v', '--verbose', action='count', dest="verbosity")
    options, args = op.parse_args()
    return dict(verbosity=options.verbosity, tests=args)

def run_tests(verbosity=0, tests=[]):
    tests = [ unittest.TestLoader().loadTestsFromTestCase(v) 
            for k,v in globals().items() 
            if k.startswith("Test") and (tests == [] or k in tests)]
    unittest.TextTestRunner(verbosity=verbosity).run(unittest.TestSuite(tests))

if __name__ == '__main__':
    run_tests(**get_args())
